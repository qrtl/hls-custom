# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_rep_title = fields.Text(
        related="company_id.purchase_rep_title", readonly=False
    )
    purchase_rep_signature = fields.Binary(
        related="company_id.purchase_rep_signature", readonly=False
    )
