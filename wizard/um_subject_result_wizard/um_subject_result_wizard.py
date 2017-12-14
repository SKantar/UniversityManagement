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

class um_subject_result_wizard(models.TransientModel):
    _name = "um.subject.result.wizard"

    student_id = fields.Many2one("um.student", "Student",default=2)
    subject_ids = fields.Many2many("um.subject",
                                   "wizard_result_subject_rel",
                                   "wizard_id",
                                   "subject_id",
                                   "Subjects")

    @api.multi
    def add_subject(self):
        self.ensure_one()

        for subject_id in self.subject_ids.ids:
            data = {
                'student_id': self.student_id.id,
                'subject_id': subject_id
            }
            self.env["um.subject.result"].create(data)
        return True
