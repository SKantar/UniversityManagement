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

TYPE_OF_STUDIES = [
    ("s", "Strukovne"),
    ("a", "Akademske"),
    ("m", "Master"),
    ("d", "Doktorske")
]

DURATION = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
]

class um_program(models.Model):
    _name = "um.program"
    _inherit = ["mail.thread", "ir.needaction_mixin"]


    name = fields.Char("Name", size=64)
    code = fields.Char("Code", size=20)
    type_of_studies = fields.Selection(TYPE_OF_STUDIES, "Type of studies")
    duration = fields.Selection(DURATION, "Duration")
    profession = fields.Char("Profession", size=120)
    faculty_id = fields.Many2one("um.faculty", "Faculty")
    description = fields.Text("Description")
    sequence_id = fields.Many2one("ir.sequence", "Sequence")
    academic_year_ids = fields.Many2many("um.academic.year",
                                         "program_year_rel",
                                         "program_id",
                                         "academic_year_id",
                                         "Academic years")
    student_ids = fields.One2many("um.student", "program_id", "Students")
    scholarship_ids = fields.Many2many("product.product",
                                       "program_schoolarship_rel",
                                       "program_id",
                                       "product_id",
                                       "Scholarships")


    @api.multi
    def show_students(self):
        context = {'student_ids' : self.student_ids.ids}
        res = self.env["ir.model.data"].get_object_reference("university_management", "action_um_student")
        return res