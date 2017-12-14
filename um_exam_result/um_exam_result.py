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

STATES = [
    ("n", "New Exam"),
    ("e", "Edit"),
]

class um_exam_result(models.Model):
    _name = "um.exam.result"


    student_id = fields.Many2one("um.student", "Student", required=True)
    exam_id = fields.Many2one("um.exam", "Exam", required = True)
    date = fields.Date("Date")
    points = fields.Integer("Points", default=0)
    is_banned = fields.Boolean("Banned")
    state = fields.Selection(STATES, string="State", readonly=True, default="n")

    @api.model
    def create(self, vals):
        return super(um_exam_result, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(um_exam_result, self).write(vals)

    @api.multi
    def unlink(self):
        return super(um_exam_result, self).unlink()