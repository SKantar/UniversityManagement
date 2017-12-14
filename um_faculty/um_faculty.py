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

class um_faculty(models.Model):
    _name = "um.faculty"
    _inherits = { "res.company": "company_id" }

    @api.model
    def _lang_get(self):
        res = self.env["res.lang"].search_read([])
        return [(r['code'], r['name']) for r in res] + [('', '')]



    company_id = fields.Many2one("res.company", "Company", ondelete="cascade", required=True)
    currency_id = fields.Many2one("res.currency", "Currency")
    code = fields.Char('Code', size=20, required=True)
    state_id = fields.Many2one("res.country.state", "State")
    program_ids = fields.One2many("um.program", "faculty_id", "Programs")
    lang = fields.Selection(_lang_get, "Language", help="If the selected language is loaded in the system, all documents related to this partner will be printed in this language. If not, it will be english.")
    teacher_ids = fields.One2many("hr.employee", "faculty_id", "Teachers")

    @api.model
    def create(self, vals):
        faculty = super(um_faculty, self).create(vals)
        user = self.env["um.main"]._create_user(vals["code"], faculty.company_id.id)
        # print faculty.company_id
        return faculty

    @api.multi
    def write(self, vals):
        return super(um_faculty, self).write(vals)

    @api.multi
    def unlink(self):
        return super(um_faculty, self).unlink()

    @api.one
    @api.depends("company_id")
    def _compute_teachers(self):
        return self.env["hr.employee"].search([("company_id", "=", self.company_id.id)])




