from odoo import models, fields, api
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    # ── Basic Info ──────────────────────────────────────────────
    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name',  required=True)

    # ── Birth Date & Age (computed) ──────────────────────────────
    birth_date = fields.Date(string='Birth Date')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,          # stored so it is searchable / sortable
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                born = rec.birth_date
                rec.age = (
                    today.year - born.year
                    - ((today.month, today.day) < (born.month, born.day))
                )
            else:
                rec.age = 0

    # ── Medical Info ─────────────────────────────────────────────
    history    = fields.Html(string='Medical History')
    cr_ratio   = fields.Float(string='CR Ratio')

    blood_type = fields.Selection(
        selection=[
            ('A+',  'A+'),
            ('A-',  'A-'),
            ('B+',  'B+'),
            ('B-',  'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+',  'O+'),
            ('O-',  'O-'),
        ],
        string='Blood Type',
    )

    pcr   = fields.Boolean(string='PCR')
    image = fields.Image(string='Patient Image')

    # ── Contact Info ─────────────────────────────────────────────
    address = fields.Text(string='Address')