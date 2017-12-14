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

class um_academic_year(models.Model):
    _name = "um.academic.year"

    name = fields.Char("Name", size=64, required=True)
    program_ids = fields.Many2many("um.program",
                                   "program_year_rel",
                                   "academic_year_id",
                                   "program_id",
                                   "Programs")
    num_of_electoral = fields.Integer('No of electoral', default=0, required=True)
    subject_ids = fields.Many2many("um.subject",
                                   "academic_year_subject_rel",
                                   "academic_year_id",
                                   "subject_id",
                                   "Subjects")