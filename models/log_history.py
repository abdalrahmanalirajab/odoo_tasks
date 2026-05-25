from odoo import fields, models

class HmsLogHistory(models.Model):
    """Read-only audit log for patient state changes."""

    _name = 'hms.log.history'
    _description = 'Patient Log History'
    _order = 'date desc'

    patient_id = fields.Many2one(
        'hms.patient',
        string='Patient',
        ondelete='cascade',
        required=True,
        readonly=True,
    )
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    description = fields.Text(
        string='Description',
        readonly=True,
    )
