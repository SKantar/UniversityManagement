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

class um_teacher(models.Model):
    _inherit = "hr.employee"
    @api.model
    def _compute_subjects(self):
        result = {}
        return result

    subject_ids = fields.Many2many("um.subject",
                                   "subject_teacher_rel",
                                   "teacher_id",
                                   "subject_id",
                                   "Subjects")

    faculty_id = fields.Many2one("um.faculty", "Faculty", compute="_calculate_faculty_id", store=True)

    @api.model
    def create(self, vals):
        user = self.env["um.main"]._create_user(vals["name"])
        vals["user_id"] = user.id
        return super(um_teacher, self).create(vals)

    @api.one
    @api.depends("company_id")
    def _calculate_faculty_id(self):
        res =  self.env["um.faculty"].search([('company_id', "=", self.company_id.id)])
        self.faculty_id = res.id



