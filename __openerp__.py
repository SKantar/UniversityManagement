{
    'name': 'University Management',
    'version': '3.0',
    'category': 'Tools',
    'summary': 'Manage Students, Faculties and Education Institute',
    'complexity': "easy",
    'description': """
            This module provide overall education management system over OpenERP
            Features includes managing
                * Student
                * Faculty
                * Programs
                * Academic years
                * Subjects
                * Teachers
                * Exams
    """,
    'author': 'skantar12',
    'website': 'https://www.facebook.com/KPETEH',
    'depends': ["base", "hr", "email_template", "crm", "web","account"],
    'data': [
                "static/src/xml/brmb.xml",
                # "payment/payment_request_view.xml",
                # "payment/request_generator.xml",
                # "invoice_generator/um_invoice_generator.xml",
                # "report/um_exam_report/results_report.xml",
                # "report/um_student_report/potvrda_report.xml",
                "security/university_management_security.xml",
                "security/ir.model.access.csv",
                "um_faculty/um_faculty.xml",
                "um_program/um_program.xml",
                "um_subject/um_subject.xml",
                "um_teacher/um_teacher.xml",
                "wizard/um_payment_unit_wizard/um_payment_unit_wizard.xml",
                # "um_student/wizard/um_payment_plan_unit_line.xml",
                "um_exam/um_exam.xml",
                # "um_exam/server_actions.xml",
                # "um_exam/um_exam_workflow.xml",
                "um_subject_result/um_subject_result.xml",
                "wizard/um_subject_result_wizard/um_subject_result_wizard.xml",
                "um_student/um_student.xml",
                "um_signed_exam/um_signed_exam.xml",
                "um_data_import/wizard/um_data_import_wizard.xml",
                # "data_import/data_importer_view.xml",
                # "data_import/data_importer.xml",

                "um_data_import/um_data_importer.xml",
                "um_exam_result/um_exam_result.xml",
                "um_academic_year/um_academic_year.xml",
                "cron_jobs/um_payment_request/um_payment_request.xml",
                "um_payment_unit/um_payment_unit.xml",
                "um_main/um_main.xml",
                "cron_jobs/cron_jobs.xml",
                "server_actions/um_exam_actions.xml",
                "reports/um_exam_signed_students_report/um_exam_signed_students_report.xml",
                "reports/um_exam_results_report/um_exam_results_report.xml"
    ],
    'css':[
        # "static/src/css/*.css",
    ],
    'js':[
        "static/src/js/university_management.js",
    ],
    'demo': [],
    'test': [],
    'qweb' : [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'images': [],

}