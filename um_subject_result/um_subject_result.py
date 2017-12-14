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
from datetime import date

class um_subject_result(models.Model):
    _name = "um.subject.result"

    student_id = fields.Many2one("um.student", "Student", required=True)
    subject_id = fields.Many2one("um.subject", "Subject", required=True)
    mark = fields.Integer("Mark", readonly=True,default=0)
    date = fields.Date("Last update", required = True, default=date.today())
    points = fields.Integer("Points", required = True, default=0)

    @api.model
    def create(self, vals):
        vals["date"] = date.today()
        return super(um_subject_result, self).create(vals)

    @api.multi
    def write(self, vals):
        vals["date"] = date.today()
        return super(um_subject_result, self).write(vals)
