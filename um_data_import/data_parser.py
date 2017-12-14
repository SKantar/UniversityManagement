FACULTY_NAME = 0
FACULTY_CODE = 1
FACULTY_STREET = 2
FACULTY_STREET2 = 3
FACULTY_CITY = 4


PROGRAM_NAME = 0
PROGRAM_CODE = 1
PROGRAM_TYPE_OF_STUDIES = 2
PROGRAM_DURACTION = 3
PROGRAM_PROFESSION = 4
PROGRAM_FACULTY  = 5
PROGRAM_DESCRIPTION = 6
PROGRAM_SEQUENCE = 7
import logging
from openerp import api
_logger = logging.getLogger(__name__)



def _int(value):
    try:
        new_value = int(value)
    except:
        new_value = False
    return new_value

def _format_value(value):
    if isinstance(value, unicode):
        new_value = value
    else:
        try:
            new_value = str(int(value))
        except:
            new_value = str(value)
    return new_value

def _collect_values(book, column_index):
    sheet = book.sheet_by_index(0)
    values = []
    for i in xrange(sheet.nrows):
        if i == 0: continue
        line = sheet.row_values(i)
        value = line[column_index]
        if value and value not in values:
            values.append(value)
    return values

def _to_lines(book):
    sheet = book.sheet_by_index(0)
    lines = []
    for i in xrange(sheet.nrows):
        if i == 0: continue
        line = sheet.row_values(i)
        lines.append(line)

    return lines

@api.model
def _load_code_items(self, model_name, column='name', domain=[]):
    dao = self.env[model_name]
    values = {}
    for res in dao.read(dao.search(domain), [column]):
        values[res[column]] = res['id']
    return values


def _string(data, column_name):
    return (str(data[column_name]) if isinstance(data[column_name], (int, long, float)) else data[column_name]).strip()

def parse_faculty(book, callback):
    lines = _to_lines(book)

    for line in lines:
        data = line

        faculty = {}
        faculty['name'] = _string(data, FACULTY_NAME)
        faculty['code'] = _string(data, FACULTY_CODE)
        faculty['street'] = _string(data, FACULTY_STREET)
        faculty['street2'] = _string(data, FACULTY_STREET2)
        faculty['city'] = _string(data, FACULTY_CODE)
        callback(faculty)

def _calculate_tos_code(tos):
    if tos == 'Strukovne': return 's'
    elif tos == 'Akademske': return 'a'
    elif tos == 'Master': return 'm'
    elif tos == 'Doktorske': return 'd'
    else:
        return False

@api.model
def _calculate_faculty_id(self, name):
    faculty_id = self.env["um.faculty"].search([('name', '=', name.strip())])
    return faculty_id and faculty_id[0].id or False

@api.model
def parse_program(self, book, callback):
    lines = _to_lines(book)

    for line in lines:
        data = line

        program = {}
        program['name'] = _format_value(data[PROGRAM_NAME])
        program['code'] = _format_value(data[PROGRAM_CODE])
        program['type_of_studies'] = _calculate_tos_code(_string(data, PROGRAM_TYPE_OF_STUDIES))
        program['duraction'] = _format_value(data[PROGRAM_DURACTION])
        program['description'] =_format_value(data[PROGRAM_DESCRIPTION])
        program['profession'] = _format_value(data[PROGRAM_PROFESSION])
        program['faculty_id'] = _calculate_faculty_id(self, data[PROGRAM_FACULTY])
        callback(program)