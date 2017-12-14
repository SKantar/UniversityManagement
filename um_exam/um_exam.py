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


EXAM_TYPE = [
    ("p", "Progress test"),
    ("e", "Exam")
]

STATES = [
    ("n", "New exam"),
    ("d", "Done"),
    ("c", "Cancelled")
]

class um_exam(models.Model):
    _name = "um.exam"

    subject_id = fields.Many2one("um.subject", string="Subject", required=True, widget="selection")
    exam_type = fields.Selection(EXAM_TYPE, string="Exam type", required=True)
    start_time = fields.Datetime("Start time")
    end_time = fields.Datetime("End date")
    state = fields.Selection(STATES, "State", default="n")
    note = fields.Text("Note")
    result_ids = fields.One2many("um.exam.result", "exam_id", "Results")
    student_ids = fields.One2many("um.signed.exam", "student_id", "Students", compute="_calculate_students")

    @api.multi
    def name_get(self):
        result = []
        for obj in self.search([]):
            name = "%s (%s)" % (obj.subject_id.name, obj.exam_type)
            result.append((obj.id, name))
        return result

    @api.multi
    def sign_exam(self, ids):
        print "MOOOOOOOOOOOOOOOOOOOOOOJ"
        print ids
        print self
        print "MOOOOOOOOOOOOOOOOOOOOOOJ"
        student = self.env["um.student"].search([("user_id", "=", self.env.uid)])
        student_id = student and student[0].id or False
        if not student_id:
            return False
        else:
            signed_exam_data = {
                "student_id" : student_id,
                "exam_id": False
            }
            for id in ids:
                signed_exam_data["exam_id"] = id
                print signed_exam_data
            #     signed_exam_data["exam_id"] = id
                self.env["um.signed.exam"].create(signed_exam_data)
            # print ids
            return True


    @api.one
    def _calculate_students(self):
        self.student_ids = self.env["um.signed.exam"].search([("exam_id","=", self.id)])
