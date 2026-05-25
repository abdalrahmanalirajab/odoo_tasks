# -*- coding: utf-8 -*-
"""Hospital patient model — Labs 1–3."""

import re
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    """Patient record with medical data, department assignment, and state logs."""

    _name = 'hms.patient'
    _description = 'Hospital Patient'
    _order = 'last_name, first_name'

    # Lab 1 — Personal & medical information
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    history = fields.Html(string='Medical History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        selection=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        string='Blood Type',
    )
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Photo', attachment=True)
    address = fields.Text(string='Address')
    state = fields.Selection(
        selection=[
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious'),
        ],
        string='State',
        default='undetermined',
    )

    # Lab 2 — Department, doctors, and log history
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain="[('is_opened', '=', True)]",
        ondelete='set null',
    )
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.capacity',
        readonly=True,
    )
    doctor_ids = fields.Many2many(
        'hms.doctor',
        string='Doctors',
    )
    log_history_ids = fields.One2many(
        'hms.log.history',
        'patient_id',
        string='Log History',
    )

    _unique_patient_email = models.Constraint(
        'unique (email)',
        'A patient with this email address already exists.',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Compute age in full years from birth_date."""
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

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        """Display name as 'First Last'."""
        for rec in self:
            rec.display_name = (
                f"{rec.first_name or ''} {rec.last_name or ''}".strip()
            )

    @staticmethod
    def _age_from_birth_date(birth_date):
        """Return age in years for a given birth date."""
        if not birth_date:
            return 0
        if isinstance(birth_date, str):
            birth_date = fields.Date.from_string(birth_date)
        today = date.today()
        return (
            today.year - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format."""
        pattern = re.compile(
            r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        )
        for rec in self:
            if rec.email and not pattern.match(rec.email):
                raise ValidationError(_('Invalid email format for patient.'))

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        """CR Ratio is mandatory when PCR is checked."""
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError(
                    _('CR Ratio is mandatory when PCR is checked.')
                )

    @api.constrains('department_id')
    def _check_department_opened(self):
        """Patient cannot be assigned to a closed department."""
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError(
                    _('You cannot assign a closed department.')
                )

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        """Auto-check PCR and warn when age is below 30."""
        age = self._age_from_birth_date(self.birth_date)
        if age and age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _(
                        'PCR has been automatically checked because '
                        'age is below 30.'
                    ),
                },
            }

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-check PCR on create when birth_date implies age < 30."""
        for vals in vals_list:
            if vals.get('birth_date') and not vals.get('pcr'):
                age = self._age_from_birth_date(vals['birth_date'])
                if age < 30:
                    vals['pcr'] = True
        return super().create(vals_list)

    def write(self, vals):
        """Log state changes automatically."""
        old_states = {rec.id: rec.state for rec in self}
        result = super().write(vals)

        if 'state' in vals:
            state_labels = dict(self._fields['state'].selection)
            LogHistory = self.env['hms.log.history']
            for rec in self:
                if old_states.get(rec.id) != rec.state:
                    LogHistory.create({
                        'patient_id': rec.id,
                        'created_by': self.env.user.id,
                        'date': fields.Datetime.now(),
                        'description': _('State changed to %s') % state_labels.get(
                            rec.state, rec.state
                        ),
                    })
        return result

    def action_set_good(self):
        """Set patient state to Good."""
        self.write({'state': 'good'})

    def action_set_fair(self):
        """Set patient state to Fair."""
        self.write({'state': 'fair'})

    def action_set_serious(self):
        """Set patient state to Serious."""
        self.write({'state': 'serious'})

    def action_reset_state(self):
        """Reset patient state to Undetermined."""
        self.write({'state': 'undetermined'})
