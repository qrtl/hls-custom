# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_uom_po_id = fields.Many2one(
        "uom.uom",
        "Purchase Unit of Measure",
        readonly=True,
        related="product_id.uom_po_id",
    )
    product_uom_po_qty = fields.Float(
        "Quantity in Purchase UoM",
        compute="_compute_product_uom_po_qty",
        store=True,
    )

    @api.multi
    @api.depends("quantity", "product_id.uom_po_id")
    def _compute_product_uom_po_qty(self):
        for quant in self:
            quant.product_uom_po_qty = quant.product_uom_id._compute_quantity(
                quant.quantity, quant.product_uom_po_id, round=False
            )
