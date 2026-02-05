# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    rep_title = fields.Char(related="company_id.rep_title", readonly=False)
    rep_signature = fields.Binary(related="company_id.rep_signature", readonly=False)
