# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    removal_date = fields.Datetime(
        readonly=True,
        index=True,
        help="Removal date of the lot/serial of the stock move. When the move "
        "holds several lots, the earliest removal date is kept.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        move_ids = {
            vals["stock_move_id"] for vals in vals_list if vals.get("stock_move_id")
        }
        removal_date_by_move = {
            move.id: move._get_removal_date()
            for move in self.env["stock.move"].browse(move_ids)
        }
        lot_ids = {vals["lot_id"] for vals in vals_list if vals.get("lot_id")}
        removal_date_by_lot = {
            lot.id: lot.removal_date for lot in self.env["stock.lot"].browse(lot_ids)
        }
        for vals in vals_list:
            if vals.get("lot_id"):
                # Layers of a lot valuated product are valued per lot.
                removal_date = removal_date_by_lot.get(vals["lot_id"])
            else:
                removal_date = removal_date_by_move.get(vals.get("stock_move_id"))
            if removal_date:
                vals["removal_date"] = removal_date
        return super().create(vals_list)
