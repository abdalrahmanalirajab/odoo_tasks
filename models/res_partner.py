from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        ondelete='set null',
    )

    @api.constrains('email')
    def _check_email_not_in_patients(self):
        """Customer email cannot duplicate any patient email."""
        for rec in self:
            if rec.email:
                patient = self.env['hms.patient'].search(
                    [('email', '=', rec.email)], limit=1
                )
                if patient:
                    raise ValidationError(
                        _('The email "%s" is already used by patient "%s %s".')
                        % (rec.email, patient.first_name, patient.last_name)
                    )

    @api.constrains('vat', 'customer_rank')
    def _check_vat_required(self):
        """Tax ID (VAT) is mandatory for customers."""
        for rec in self:
            if rec.customer_rank and rec.customer_rank > 0 and not rec.vat:
                raise ValidationError(
                    _('Tax ID (VAT) is mandatory for customer "%s".') % rec.name
                )

    def unlink(self):
       
        for rec in self:
            if rec.related_patient_id:
                raise UserError(
                    _('Cannot delete customer "%s" because they are linked to '
                      'patient "%s %s". Remove the patient link first.')
                    % (
                        rec.name,
                        rec.related_patient_id.first_name,
                        rec.related_patient_id.last_name,
                    )
                )
        return super().unlink()
