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

class um_signed_exam(models.Model):
    _name = "um.signed.exam"

    student_id = fields.Many2one("um.student", "Student")
    exam_id = fields.Many2one("um.exam", "Exam")
    # name = fields.Char("Name", related="exam_id")
    subject_id = fields.Many2one("um.subject", related="exam_id.subject_id")
    start_time = fields.Datetime("Start time", related="exam_id.start_time")
    end_time = fields.Datetime("End time", related="exam_id.end_time")
    note = fields.Text("Note", related="exam_id.note")