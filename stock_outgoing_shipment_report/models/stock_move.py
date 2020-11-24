# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_secondary_uom_qty(self):
        self.ensure_one()
        secondary_uom = self.sale_line_id and self.sale_line_id.secondary_uom_id or self.product_id.sale_secondary_uom_id
        if not secondary_uom:
            return
        factor = secondary_uom.factor * self.product_uom.factor
        return int(self.quantity_done / (factor or 1.0))
