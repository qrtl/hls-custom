# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("qty_invoiced", "product_id.is_amount_adj_product")
    def _compute_qty_delivered(self):
        res = super()._compute_qty_delivered()
        for line in self:
            if line.product_id.is_amount_adj_product:
                if line.qty_invoiced < 0:
                    line.qty_delivered = line.qty_invoiced
        return res
