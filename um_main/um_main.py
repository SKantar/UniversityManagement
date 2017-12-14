# -*- encoding: utf-8 -*-
#                                                                            #
#   OpenERP Module                                                           #
#   Copyright (C) 2013 Author <email@email.fr>                               #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU Affero General Public License as           #
#   published by the Free Software Foundation, either version 3 of the       #
#   License, or (at your option) any later version.                          #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Affero General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Affero General Public License #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                            #
from openerp import fields, models, api
from openerp import netsvc
import base64
import tempfile
import os
import os.path
from subprocess import call
from datetime import date
import pdfkit
ATTACHEMENT_NAME = 0
ATTACHEMENT_CONTENT = 1

class um_main(models.AbstractModel):
    _name = "um.main"

    @api.returns("res.users")
    def _create_user(self, name, company_id = None):
        user = {}
        user["login"] = name
        user["new_password"] = name
        user["name"] = name

        if company_id:
            user["company_ids"] = [(4, company_id)]
            user["company_id"] = company_id
        return self.env["res.users"].create(user)


    @api.multi
    def _create_pdf_report_for_invoices(self, invoice_ids, encode=True):
        # report_service = 'report.account.invoice'
        # service2 = netsvc.LocalService(report_service)
        # service = netsvc.LocalService("report.account.report_invoice")
        #
        # datas = {
        #     'form' : {
        #         'response_ids' : invoice_ids,
        #         'orientation' : 'vertical',
        #         'paper_size' : "a4",
        #         'page_number' : True,
        #         'without_pagebreak' : False
        #     }
        # }
        report = self.env["report"]._get_report_from_name("account.report_invoice")
        invoices = self.env["account.invoice"].browse(invoice_ids)
        # res = self.env['report'].get_action(invoice_ids[0], "account.report_invoice")
        # docargs = {
        #     "doc_ids": invoice_ids,
        #     "doc_model": report.model,
        #     "docs": reports
        # }

        pdf = self.env["report"].get_pdf(invoices, "account.report_invoice")
        # tmp = self.env["report"].render("account.report_invoice", docargs)
        # tmp = unicode(tmp, 'UTF-8')
        # tmp = base64.b64encode(tmp)
        # pdfkit.from_string(tmp, "bulja.pdf")
        # return res
        # (pdf, format) = service.create(invoice_ids, datas)
        #
        if encode:
           pdf = base64.b64encode(pdf)
        return pdf
    @api.multi
    def _create_zip_for_invoices(self, invoice_ids):
        invoices = self.env["account.invoice"].browse(invoice_ids)
        grouped_invoices = {}
        for invoice in invoices:
            key = (invoice.partner_id.id, invoice.partner_id.name)
            if key not in grouped_invoices.keys():
                grouped_invoices[key] = [invoice.id]
            else:
                grouped_invoices[key].append(invoice.id)

        tmp_dir_name = tempfile.mkdtemp()
        if not os.path.exists(tmp_dir_name):
            os.makedirs(tmp_dir_name)

        invoices_dir_name = '%s/invoices' % tmp_dir_name
        os.makedirs(invoices_dir_name)

        for key, value in grouped_invoices.iteritems():
            pdf_report = self._create_pdf_report_for_invoices(value, False)
            file_name = key[1].replace('/','-')
            with open("%s/%s.pdf" % (invoices_dir_name, file_name), "w") as f:
                f.write(pdf_report)

        zip_file_name = "%s/invoices.zip" % tmp_dir_name

        call(["zip", "-r", zip_file_name, invoices_dir_name])

        with open(zip_file_name, "r") as f:
            zip_data = f.read()

        zip_data = base64.b64encode(zip_data)

        return zip_data

    @api.multi
    def _create_email_for_invoice(self, res_id, partner_email, template_id ):
        values = self.env["email.template"].generate_email(template_id, res_id)
        attachments = []
        for value in values['attachments']:
            attachment_data = {
                    'name': value[ATTACHEMENT_NAME],
                    'datas_fname': value[ATTACHEMENT_NAME],
                    'datas': value[ATTACHEMENT_CONTENT],
                    'res_model': 'account.invoice',
                    'res_id': res_id,
            }
            attachments.append(self.env["ir.attachment"].create(attachment_data))

        post_values = {
            'subject': values['subject'],
            'body': values['body'],
            #'parent_id': wizard.parent_id and wizard.parent_id.id,
            #'partner_ids': [(4, partner.id) for partner in wizard.partner_ids],
            'attachments': [(attach.datas_fname or attach.name, base64.b64decode(attach.datas)) for attach in attachments],
        }

        # message_id = self.env["account.invoice"].message_post(  [res_id],
        #                                                         type='email',
        #                                                         subtype='mt_comment',
        #                                                         **post_values)

        mail_values = {
            # 'mail_message_id': message_id,
            'email_to': partner_email,
            'auto_delete': True,
            'body_html': post_values['body'],
            'state': 'outgoing'
        }

        return self.env["mail.mail"].create(mail_values)