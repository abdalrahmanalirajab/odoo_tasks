# -*- coding: utf-8 -*-
"""Hospital doctor model."""

from odoo import api, fields, models


class HmsDoctor(models.Model):
    """Doctor assigned to a hospital department."""

    _name = 'hms.doctor'
    _description = 'Hospital Doctor'
    _order = 'last_name, first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Photo', attachment=True)
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        ondelete='set null',
    )

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        """Build display name from first and last name."""
        for rec in self:
            rec.display_name = (
                f"{rec.first_name or ''} {rec.last_name or ''}".strip()
            )
