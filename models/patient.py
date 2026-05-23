from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    # ── Basic Info ───────────────────────────────────────────
    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name',  required=True)

    # ── Birth Date & Age ─────────────────────────────────────
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                born = rec.birth_date
                rec.age = (today.year - born.year
                           - ((today.month, today.day) < (born.month, born.day)))
            else:
                rec.age = 0

    # ── Medical Info ─────────────────────────────────────────
    history   = fields.Html(string='Medical History')
    cr_ratio  = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
        ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'),
    ], string='Blood Type')
    pcr   = fields.Boolean(string='PCR')
    image = fields.Image(string='Patient Image')

    # ── Contact Info ─────────────────────────────────────────
    address = fields.Text(string='Address')

    # ── State ────────────────────────────────────────────────
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good',         'Good'),
        ('fair',         'Fair'),
        ('serious',      'Serious'),
    ], string='State', default='undetermined')

    # ── Department (Many2one) ─────────────────────────────────
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain="[('is_opened', '=', True)]",
    )
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.capacity',
        readonly=True,
    )

    # ── Doctors (Many2many) ───────────────────────────────────
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')

    # ── Log History (One2many) ────────────────────────────────
    log_ids = fields.One2many('hms.log', 'patient_id', string='Log History')

    # ── Auto-check PCR if age < 30 ────────────────────────────
    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Automatically Checked',
                    'message': 'PCR has been automatically checked because the patient age is under 30.',
                }
            }

    # ── Log when state changes ────────────────────────────────
    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            self.log_ids = [(0, 0, {
                'created_by': self.env.user.id,
                'date':       date.today(),
                'description': f'State changed to {dict(self._fields["state"].selection).get(self.state)}',
            })]

    # ── Validation: CR ratio required if PCR checked ──────────
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError('CR Ratio is required when PCR is checked!')
