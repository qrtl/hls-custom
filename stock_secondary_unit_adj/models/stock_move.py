# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        res = super().action_show_details()
        if self.secondary_uom_id:
            res["context"]["secondary_uom_id"] = self.secondary_uom_id.id
        return res
