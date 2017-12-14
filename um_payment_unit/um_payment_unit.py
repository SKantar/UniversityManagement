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

from openerp import models, fields, api
SEND_INVOICE_BY = [
    ("p", "Post"),
    ("e", "Email")
]
class um_payment_unit(models.Model):
    _name = "um.payment.unit"

    product_id = fields.Many2one("product.product", "Product", readonly=True)
    partner_id = fields.Many2one("res.partner", "Partner", readonly=True)
    name = fields.Char("Name", size=64)
    price_unit = fields.Float("Price Unit", readonly=True)
    quantity = fields.Float("Quantity")
    discount = fields.Float("Discount")
    date = fields.Date("Date")
    amount = fields.Float("Amount", readonly=True)
    send_invoice_by = fields.Selection(SEND_INVOICE_BY, "Send invoice by")
    invoice_id = fields.Many2one("account.invoice", "Invoice")