from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    # Basic Info
    first_name = fields.Char(
        string='First Name',
        required=True
    )

    last_name = fields.Char(
        string='Last Name',
        required=True
    )

    # Birth Date & Age
    birth_date = fields.Date(string='Birth Date')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()

        for rec in self:
            if rec.birth_date:
                born = rec.birth_date

                rec.age = (
                    today.year
                    - born.year
                    - (
                        (today.month, today.day)
                        < (born.month, born.day)
                    )
                )
            else:
                rec.age = 0

    # Medical Info
    history = fields.Html(string='Medical History')

    cr_ratio = fields.Float(string='CR Ratio')

    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Blood Type')

    pcr = fields.Boolean(string='PCR')

    image = fields.Image(string='Patient Image')

    # Contact
    address = fields.Text(string='Address')

    # State
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ],
        string='State',
        default='undetermined'
    )

    # Department
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

    # Doctors
    doctor_ids = fields.Many2many(
        'hms.doctors',
        string='Doctors'
    )

    # Logs
    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id',
        string='Log History'
    )

    # Auto-check PCR
    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.age and self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': 'Warning',
                    'message':
                    'PCR has been automatically checked because age is under 30.',
                }
            }

    # CR Ratio Validation
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and rec.cr_ratio <= 0:
                raise ValidationError(
                    'CR Ratio must be greater than 0 when PCR is checked!'
                )

    # State Change Logging
    def write(self, vals):

        old_states = {
            rec.id: rec.state
            for rec in self
        }

        result = super().write(vals)

        if 'state' in vals:

            state_labels = dict(
                self._fields['state'].selection
            )

            for rec in self:

                if old_states[rec.id] != rec.state:

                    new_label = state_labels.get(
                        rec.state,
                        rec.state
                    )

                    self.env['hms.patient.log'].create({
                        'patient_id': rec.id,
                        'created_by': self.env.user.id,
                        'date': fields.Datetime.now(),
                        'description':
                            f'State changed to {new_label}',
                    })

        return result