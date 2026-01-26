# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    is_delivery_slip_required = fields.Boolean(
        compute="_compute_is_delivery_slip_required", store=True
    )

    @api.depends("partner_id.is_delivery_slip_required")
    def _compute_is_delivery_slip_required(self):
        for move in self:
            move.is_delivery_slip_required = move.partner_id.is_delivery_slip_required
