# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AttendanceSheet(models.Model):
    """Defining Monthly Attendance sheet Information."""

    _description = "Attendance Sheet"
    _name = "attendance.sheet"

    name = fields.Char(string='Name', required=True,)
    
    date = fields.Date("Date", help="Current Date", default=fields.Date.context_today)
    attendance_type = fields.Selection(
        [("daily", "FullDay"), ("lecture", "Lecture Wise")],
        "Type",
        help="Select attendance type",
    )
    
    absent = fields.Boolean('absent')

    student_list_2 = fields.Many2many('student','filiere_id',string='Student List')
    
    