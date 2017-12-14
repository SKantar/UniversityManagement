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

class um_subject(models.Model):
    _name = "um.subject"

    name = fields.Char("Name", size = 64, required = True)
    code = fields.Char("Code", size = 20, required = True)
    description = fields.Text("Description")
    is_mandatory = fields.Boolean("Mandatory")
    espb = fields.Integer("ESPB", required = True)
    hours = fields.Integer("Hours", required = True)
    academic_year_ids = fields.Many2many("um.academic.year",
                                         "academic_year_subject_rel",
                                         "subject_id",
                                         "academic_year_id",
                                         "Academic years")
    teacher_ids = fields.Many2many("hr.employee",
                                   "subject_teacher_rel",
                                   "subject_id",
                                   "teacher_id",
                                   "Teachers")
