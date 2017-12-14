from openerp import fields, models, api
import logging
import traceback
from contextlib import contextmanager
import openerp
from openerp.modules.registry import RegistryManager

DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S.%f"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)

TEMPLATE_ID = 7
MONTHS_DIFFERENCE = 3
_logger = logging.getLogger(__name__)

TEMPLATE_ID = 7

class um_invoice_generator(models.Model):
    _name = 'um.invoice.generator'

    def update_request_state(self, request_id, state):
        """
        Update request state via separate db connection
        """
        # with self.session(self.env.cr.dbname) as session:
        self.env['um.payment.request'].browse(request_id).state = state

    # def update_file(self, request_id, file):
    #     """
    #     Update request file via separate db connection
    #     """
    #     with self.session(cr.dbname) as session:
    #         self.pool.get('um.payment.request').write(session, uid, request_id, {'downloads' : file})

    # def create_mail(self, cr, uid, param_a, param_b, param_c):
    #      with self.session(self.env.cr.dbname) as session:
    #         return self.pool.get('um.invoice.sender')._create_email_for_invoice(session, uid, [],param_a, param_b, param_c, context=None)
    #
    # def update_emails(self, cr, uid, request_id, email_ids):
    #     """
    #     Update request file via separate db connection
    #     """
    #     with self.session(cr.dbname) as session:
    #         self.pool.get('um.payment.request').write(session, uid, request_id, {'emails' : [(6, 0, email_ids)]})

    # def update_request_atempt(self, request_id, attempt):
    #     """
    #     Update request atempt in a separate db connection
    #     """
    #     with self.session(self.env.cr.dbname) as session:
    #         self.env['um.payment.request'].write(session, request_id, { 'attempt' : attempt + 1 } )
    #         return attempt + 1

    def _create_log(self, vals):
        """
        Create requestion log in a separate db connection.
        """
        with self.session(self.env.cr.dbname) as session:
            self.env['um.payment.request.log'].create( vals )

    @contextmanager
    def session(self, db_name):
        """ Context Manager: start a new session and ensure that the
        session's cursor is:

        * rollbacked on errors
        * commited at the end of the ``with`` context when no error occured
        * always closed at the end of the ``with`` context
        * it handles the registry signaling
        """
        db = openerp.sql_db.db_connect(db_name)
        cr = db.cursor()

        try:
            RegistryManager.check_registry_signaling(db_name)
            yield cr
            RegistryManager.signal_caches_change(db_name)
        except:
            cr.rollback()
            raise
        else:
            cr.commit()
        finally:
            cr.close()

    @api.model
    def _create_invoice(self):
        requests = self.env["um.payment.request"].search([('state', '=', 'confirmed')])
        request_attempt = 0
        for request in requests:
            try:
                self.update_request_state(request.id, "processing")
                for payment_unit in request.unit_ids:
                    self._create_invoice_unit(payment_unit)

                post_invoices = []
                email_invoices = []
                for payment_unit in request.unit_ids:
                    if payment_unit.send_invoice_by == "p":
                        post_invoices.append(payment_unit.invoice_id.id)
                    else:
                        email = self.env["um.main"]._create_email_for_invoice(payment_unit.invoice_id.id, payment_unit.partner_id.email, TEMPLATE_ID)
                        email_invoices.append(email.id)
                request.emails = [(6, 0 , email_invoices)]

                # request.filename = "request"+str(request.id)+".pdf"
                # _logger.info("================================")
                # _logger.info(post_invoices)
                # _logger.info("================================")
                # request.downloads = self.env["um.main"]._create_pdf_report_for_invoices(post_invoices)

                request.filename = "request"+str(request.id)+".zip"
                request.downloads = self.env["um.main"]._create_zip_for_invoices(post_invoices)


                self.update_request_state(request.id, "processed")
            except Exception, ex:
                self.update_request_state(request.id, 'error')
                error_message = str(ex)
                stack_trace = traceback.format_exc()
                self._create_log({'request_id': request.id, 'attempt': request_attempt, 'message': error_message, 'stack_trace': stack_trace, 'state': 'error'})

    @api.model
    def _create_invoice_unit(self, payment_unit):
        invoice_line_data = {
            'product_id' : payment_unit.product_id.id,
            'quantity' : payment_unit.quantity,
            'discount' : payment_unit.discount,
            'amount' : payment_unit.amount,
            'partner_id':  payment_unit.partner_id.id,
            'name': payment_unit.name,
            'price_unit': payment_unit.price_unit,
        }

        invoice = {
            'invoice_line' : [(0, 0, invoice_line_data)],
            'partner_id' : payment_unit.partner_id.id,
            'name' : payment_unit.name,
            'account_id' : 8,
            'state': 'open'
        }

        res = self.env["account.invoice"].create(invoice)
        payment_unit.invoice_id = res.id