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

from openerp import models, fields, api, exceptions
import openerp
from datetime import date
from openerp.tools import image_colorize, image_resize_image_big

GENDER = [
    ("m", "Male"),
    ("f", "Female")
]

SEND_INVOICE_BY = [
    ("p", "Post"),
    ("e", "Email")
]

STATES = [
    ("n", "New"),
    ("e", "Edit")
]

class um_student(models.Model):
    _name = "um.student"

    _inherits = {"res.users": "user_id"}
    _inherit = ["mail.thread", "ir.needaction_mixin"]
    
    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True, ondelete="cascade", auto_join=True)
    pid = fields.Char("Student ID", size=64, help="Personal IDentification Number", default=lambda l: "PIN "+l._get_user_number()+" / "+ date.today().strftime('%Y'))
    student_name = fields.Char(string="Name", related="user_id.partner_id.name")
    student_phone = fields.Char(string="Phone", related="user_id.partner_id.phone")
    student_mobile = fields.Char(string="Mobile", related="user_id.partner_id.mobile")
    student_email = fields.Char(string="Email", related="user_id.partner_id.email")
    student_website = fields.Char(string="Website", related="user_id.partner_id.website")
    contact_phone1 = fields.Char("Phone no.", size=20)
    contact_mobile1 = fields.Char("Mobile no.", size=20)
    photo = fields.Binary("Photo", default=lambda l: l._get_default_image())
    middle = fields.Char("Middle Name", size=64, required=True)
    last = fields.Char("Surname", size=64, required=True)
    gender = fields.Selection(GENDER, "Gender", default="m")
    street = fields.Char("Street", size=128)
    street2 = fields.Char("Street2", size=128)
    zip = fields.Char("Zip", size=24)
    city = fields.Char("City", size=128)
    state_id = fields.Many2one("res.country.state", "State")
    year_of_studies = fields.Many2one("um.academic.year", "Academic year", required=True)
    admission_year = fields.Integer("Admission year", required=True, default=int(date.today().strftime('%Y')))
    country_id = fields.Many2one("res.country", "Country", required=True)
    birthdate = fields.Date("Birthdate", size=64, required=True)
    school_id = fields.Many2one("um.faculty", "Faculty", required=True)
    program_id = fields.Many2one("um.program", "Program", required=True)
    student_id = fields.Many2one("um.student", "Student")
    send_invoice_by = fields.Selection(SEND_INVOICE_BY, "Sent invoices by", default="e")
    state = fields.Selection(STATES, string="State", readonly=True, default="n")
    passed_subject_ids = fields.One2many("um.subject.result", "student_id", "Passed subjects", compute="_compute_subjects", multi="all")
    unpassed_subject_ids = fields.One2many("um.subject.result", "student_id", "Unpassed subjects", compute="_compute_subjects", multi="all")
    display_name = fields.Char(string='Name', compute='_compute_display_name')
    # passed_subject_ids = fields.


    @api.model
    def create(self, vals):
        if vals.get("student_name", False):
            vals["name"] = vals["student_name"]
            vals["login"] = vals["student_name"]
            vals["new_password"] = vals["student_name"]
        else:
            exceptions.ValidationError('No data to update!')
        vals["state"] = "e"
        vals["customer"] = True
        vals["image"] = vals["photo"]

        sequence_id = self.env["um.program"].browse(vals["program_id"]).sequence_id.id
        vals["pid"] = self.env["ir.sequence"].next_by_id(sequence_id)

        student = super(um_student, self).create(vals)

        if "year_of_studies" in vals.keys():
            self._add_subject_for_year(student.id, vals["year_of_studies"])

        return student

    @api.multi
    def write(self, vals):
        if "year_of_studies" in vals.keys():
            self._add_subject_for_year(self.id, vals["year_of_studies"])
        return super(um_student, self).write(vals)

    @api.model
    def _get_default_image(self):
       image = image_colorize(open(openerp.modules.get_module_resource('base', 'static/src/img', 'avatar.png')).read())
       return image_resize_image_big(image.encode('base64'))

    @api.model
    def _get_user_number(self):
         return str(self.env["res.users"].search_count([]) + 1).zfill(2)

    @api.one
    def _compute_subjects(self):
        self.unpassed_subject_ids = self.env["um.subject.result"].search(["&",("student_id", "=", self.id), ("mark", "<", 6)])
        self.passed_subject_ids = self.env["um.subject.result"].search(["&",("student_id", "=", self.id), ("mark", ">=", 6)]).ids

    @api.model
    def _add_subject_for_year(self, student_id, year_id):
        subject_ids = self.env["um.academic.year"].browse(year_id).subject_ids.ids
        print "===================="
        print subject_ids
        print "===================="
        self._add_subjects_to_student(student_id, subject_ids)

    @api.model
    def _add_subjects_to_student(self,student_id, ids):
        subject_result_data = {
            "student_id": student_id
        }
        for id in ids:
            subject_result_data["subject_id"] = id
            self.env["um.subject.result"].create(subject_result_data)

    @api.one
    @api.depends("pid", "student_name", "last", "middle")
    def _compute_display_name(self):
        name = "%s %s, %s, %s" % (self.pid, self.student_name, self.middle, self.last)
        self.display_name = name

    # @api.multi
    # def name_get(self):
    #     res = []
    #     for obj in self.search([]):
    #         res.append((obj.id, obj.display_name))
    #     return res

    @api.multi
    def add_subject_action(self):
        self.ensure_one()
        model = self.env["ir.model.data"].get_object_reference("university_management", "view_form_um_subject_result_wizard")
        # print model[1]
        # print "blabla"
        context=self.env.context
        dict(context).update({"default_student_id" : self.id})
        print self.id
        return {
           'type': 'ir.actions.act_window',
           'name': 'Add subjects',
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': model[1],
           'res_model': 'um.subject.result.wizard',
           'nodestroy': True,
           # 'res_id': this.id, # assuming the many2one
           'target':'new',
           'context': context,
        }

        # return True

