from openerp import fields, models, api

class um_res_user(models.Model):
    _inherit = "res.users"

    student_id = fields.Many2one("um.student", "Student", compute="_get_student")

    @api.multi
    def _get_student(self):
       self.student_id = self.env["um.student"].search([('user_id', '=', self.id)]).id

    @api.multi
    def _get_registered_exams(self):
        results =self.env['um.signed.exam'].search([('student_id', '=', self.student_id)])
        exams=[]
        for obj in results:
            exams.append(obj.exam_id.id)
        return exams

um_res_user()



