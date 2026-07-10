# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    vendor_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        readonly=True,
        index=True,
        help="Vendor of the purchase order linked to the stock move, if any.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        move_ids = {
            vals["stock_move_id"] for vals in vals_list if vals.get("stock_move_id")
        }
        vendor_by_move = {
            move.id: move.purchase_line_id.order_id.partner_id.id
            for move in self.env["stock.move"].browse(move_ids)
        }
        for vals in vals_list:
            vendor_id = vendor_by_move.get(vals.get("stock_move_id"))
            if vendor_id:
                vals["vendor_id"] = vendor_id
        return super().create(vals_list)
