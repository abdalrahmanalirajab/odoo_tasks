
"""Hospital department model."""

from odoo import fields, models


class HmsDepartment(models.Model):
    """Hospital department with capacity and assigned staff."""

    _name = 'hms.department'
    _description = 'Hospital Department'
    _order = 'name'

    name = fields.Char(string='Department Name', required=True)
    capacity = fields.Integer(string='Capacity')
    is_opened = fields.Boolean(string='Is Opened', default=True)

    patient_ids = fields.One2many(
        'hms.patient',
        'department_id',
        string='Patients',
    )
    doctor_ids = fields.One2many(
        'hms.doctor',
        'department_id',
        string='Doctors',
    )
