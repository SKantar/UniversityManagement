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

REQUEST_STATES = [
    ('draft','Draft'),
    ('confirmed','Confirmed'),
    ('processing', 'Processing'),
    ('processed', 'Processed'),
    ('error', 'Error'),
]

class um_data_import_request(models.Model):
    _name = "um.data.import.request"
    create_date = fields.Datetime("Date Created", readonly=True)
    create_uid = fields.Many2one("res.users", "Created by", required=True)
    attempt = fields.Integer("Import attempt", default=1)
    model = fields.Char("Model", size=64)
    state = fields.Selection(REQUEST_STATES, "State", required=True, default="confirmed")
    data = fields.Binary("File", required=True)
    log_ids = fields.One2many("um.data.import.request.log", "request_id", "Logs")

    @api.multi
    def validate_request(self):
        self.ensure_one()
        self.state = "confirmed"

    @api.multi
    def requeue_request(self):
        self.ensure_one()
        self.state = "confirmed"
        self.attempt += 1

LOG_TYPES = [
    ('warning','Warning'),
    ('error','Error'),
]

class um_data_import_log(models.Model):
    _name = "um.data.import.request.log"

    _rec_name = "log_type"
    _order = "attempt desc, log_type"

    request_id = fields.Many2one("um.data.import.request", "Request", ondelete="cascade")
    attempt = fields.Integer("Attempt")
    partner_id = fields.Many2one("res.partner", "Site")
    message = fields.Text("Message")
    stack_trace = fields.Text("Stack Trace")
    log_type = fields.Selection(LOG_TYPES, "Log Type", default="error")


from xlrd import open_workbook
from data_parser import parse_faculty, parse_program
import logging
from openerp import SUPERUSER_ID
import base64
import datetime
import traceback
from contextlib import contextmanager
import openerp
from openerp.modules.registry import RegistryManager

DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S.%f"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)

MONTHS_DIFFERENCE = 3
_logger = logging.getLogger(__name__)

class um_data_import(models.Model):
    _name = "um.data.import"
    def update_request_state(self, request_id, state):
        """
        Update request state via separate db connection
        """
        # with self.session(self.env.cr.dbname) as session:
        self.env['um.data.import.request'].browse(request_id).state = state

    def _create_log(self, vals):
        """
        Create requestion log in a separate db connection.
        """
        self.env['um.data.import.request.log'].create( vals )

    @api.model
    def _import_data(self):
        requests = self.env["um.data.import.request"].search([('state', '=', 'confirmed')])
        request_attempt = 0
        for request in requests:
            try:
                self.update_request_state(request.id, "processing")
                data = base64.decodestring(request.data)
                book = open_workbook(file_contents=data)
                dict(self.env.context).update({"request" : request.id})

                if request.model == 'f':
                    parse_faculty(self, book, self._import_parsed_data_faculty)
                elif request.model == 'p':
                    parse_program(self, book, self._import_parsed_data_program)

                self.update_request_state(request.id,  'processed')
            except Exception, ex:
                self.update_request_state(request.id, 'error')
                error_message = str(ex)
                stack_trace = traceback.format_exc()
                self._create_log({'request_id': request.id, 'attempt': request_attempt, 'message': error_message, 'stack_trace': stack_trace, 'state': 'error'})
        return True

    @api.model
    def _import_parsed_data_faculty(self, faculty):
        self.env["um.faculty"].create(faculty)

    @api.model
    def _import_parsed_data_program(self, program):
        self.env["um.program"].create(program)