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
from datetime import datetime

STATES = [
    ("s1", "Step 1"),
    ("s2", "Step 2")
]

SEND_INVOICE_BY = [
    ("p", "Post"),
    ("e", "Email")
]

class um_payment_unit_line_wizard(models.TransientModel):
    _name = "um.payment.unit.line.wizard"

    wizard_id = fields.Many2one("um.payment.unit.wizard")
    price_unit = fields.Float("Price")
    quantity = fields.Float("Quantity")
    discount = fields.Float("Discount")
    date = fields.Date("Date")
    amount = fields.Float("Amount")

    @api.model
    def create(self, vals):
        return super(um_payment_unit_line_wizard, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(um_payment_unit_line_wizard, self).write(vals)


class um_payment_unit_wizard(models.TransientModel):
    _name = "um.payment.unit.wizard"

    student_id = fields.Many2one("um.student", "Student")
    scholarship = fields.Many2one("product.product", string="Scholarship")
    number_of_installments = fields.Integer("Number of installments", default=1)
    discount = fields.Float("Discount(%)", default=30.0)
    um_payment_unit_line_wizard_ids = fields.One2many("um.payment.unit.line.wizard", "wizard_id", "Lines")
    state = fields.Selection(STATES, default="s1")
    send_invoice_by = fields.Selection(SEND_INVOICE_BY, "Send invoice by")


    @api.multi
    def create_invoices(self):
        self.ensure_one()
        for obj in self.um_payment_unit_line_wizard_ids:
            payment_unit_data={
                'product_id': self.scholarship.id,
                'partner_id': self.student_id.user_id.partner_id.id,
                'name': self.scholarship.name_template,
                'price_unit': obj.price_unit,
                'quantity': obj.quantity,
                'discount': obj.discount,
                'date': obj.date,
                'amount': obj.amount,
                'send_invoice_by': self.send_invoice_by
            }
            self.env["um.payment.unit"].create(payment_unit_data)
        return True

    @api.multi
    def action_next(self):
        self.ensure_one()
        self.state="s2"
        for i in xrange(self.number_of_installments):
            um_payment_unit_line_data = {
                'price_unit': self.scholarship.list_price,
                'quantity': 1.0 / self.number_of_installments,
                'discount':  self.discount,
                'date': datetime.today(),
                'amount': self.scholarship.list_price / self.number_of_installments * (1 - self.discount / 100 )
            }
            self.um_payment_unit_line_wizard_ids = [(0,0,um_payment_unit_line_data)]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'um.payment.unit.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
             }

    @api.multi
    def action_previous(self):
        self.ensure_one()
        self.state="s1"
        self.um_payment_unit_line_wizard_ids = [(5,False, False)]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'um.payment.unit.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
             }

