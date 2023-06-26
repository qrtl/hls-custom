# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    @api.depends(
        "qty_invoiced",
        "qty_delivered_method",
        "qty_delivered_manual",
        "analytic_line_ids.so_line",
        "analytic_line_ids.unit_amount",
        "analytic_line_ids.product_uom_id",
    )
    def _compute_qty_delivered(self):
        res = super()._compute_qty_delivered()
        for line in self:
            if line.qty_invoiced < 0:
                line.qty_delivered = line.qty_invoiced
        return res
