from openerp import models, fields, api

REQUEST_STATES = [
    ('draft','Draft'),
    ('confirmed','Confirmed'),
    ('processing', 'Processing'),
    ('processed', 'Processed'),
    ('error', 'Error'),
]

class um_payment_request(models.Model):
    _name = "um.payment.request"

    create_date = fields.Datetime("Date Created", readonly=True)
    create_uid = fields.Many2one("res.users", "Created by", required=True)
    attempt = fields.Integer("Import attempt", default=1)
    unit_ids = fields.Many2many("um.payment.unit",
                                "payment_unit_request_rel",
                                "request_id",
                                "unit_id",
                                "Units")
    state = fields.Selection(REQUEST_STATES, "State", required=True, default="confirmed")
    downloads = fields.Binary("Downloads")
    filename = fields.Char("Filename", default="example.zip")
    emails = fields.Many2many("mail.mail",
                              "request_mail_rel",
                              "request_id",
                              "mail_id",
                              "Mails")
    log_ids = fields.One2many("um.payment.request.log", "request_id", "Logs")

    @api.multi
    def validate_request(self):
        self.ensure_one()
        self.state = "confirmed"

    @api.multi
    def requeue_request(self):
        self.ensure_one()
        self.state = "confirmed"
        self.attempt += 1

LOG_TYPES = [
    ('warning','Warning'),
    ('error','Error'),
]

class um_payment_request_log(models.Model):
    _name = "um.payment.request.log"

    _rec_name = "log_type"
    _order = "attempt desc, log_type"

    request_id = fields.Many2one("um.payment.request", "Request", ondelete="cascade")
    attempt = fields.Integer("Attempt")
    partner_id = fields.Many2one("res.partner", "Site")
    message = fields.Text("Message")
    stack_trace = fields.Text("Stack Trace")
    log_type = fields.Selection(LOG_TYPES, "Log Type", default="error")

from datetime import date
import openerp
from contextlib import contextmanager
from openerp.modules.registry import RegistryManager
from dateutil.relativedelta import relativedelta
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S.%f"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)
import logging
_logger = logging.getLogger(__name__)

class um_make_requests(models.Model):
    _name = "um.make.requests"

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
    def _make_request(self):
        start_date = date.today() + relativedelta(months=-1)
        end_date = date.today()

        units = self.env["um.payment.unit"].search(["&", ('date','<=',end_date.strftime(DEFAULT_SERVER_DATE_FORMAT)),('date','>',start_date.strftime(DEFAULT_SERVER_DATE_FORMAT))]).ids
        _logger.info(units)
        try:
            with self.session(self.env.cr.dbname) as session:
                request_data = {
                    'create_date': date.today(),
                    'create_uid': self.env.uid,
                    'unit_ids': [(6, 0, units)]
                }
                # _logger.info('====================================')
                self.env["um.payment.request"].create(request_data)
                # self.pool.get('um.payment.request').create(cr, uid, request, context=context)
        except Exception, ex:
            pass