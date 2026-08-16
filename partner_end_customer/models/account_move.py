# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    end_customer = fields.Char(
        compute="_compute_end_customer",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id")
    def _compute_end_customer(self):
        for move in self:
            move.end_customer = move.partner_id.end_customer
