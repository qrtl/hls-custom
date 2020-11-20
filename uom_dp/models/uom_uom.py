# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class UoM(models.Model):
    _inherit = "uom.uom"

    uom_dp = fields.Char("Demical Places", compute="_compute_uom_dp")

    @api.multi
    def _compute_uom_dp(self):
        for uom in self:
            uom.uom_dp = str(uom.rounding)[::-1].find(".")
