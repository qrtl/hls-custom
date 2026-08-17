# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockLot(models.Model):
    _inherit = "stock.lot"

    def write(self, vals):
        # removal_date is a stored computed field of product_expiry, so it also
        # changes as a side effect of writing expiration_date or product_id.
        # Such a recomputation is flushed through _write_multi() and never
        # reaches this override, hence the comparison of the values before and
        # after the write rather than a lookup of the key in vals.
        previous_dates = {lot.id: lot.removal_date for lot in self}
        res = super().write(vals)
        realigned = self.filtered(
            lambda lot: lot.removal_date != previous_dates[lot.id]
        )
        if realigned:
            realigned._update_layer_removal_date()
        return res

    def _update_layer_removal_date(self):
        """Realign the valuation layers that took their removal date from these
        lots, as the layers store it instead of reading it from the lots.

        sudo() is needed because stock.valuation.layer is only writable by stock
        managers, while the dates of a lot are maintained by any stock user. It
        also lets the realignment reach the layers of the other companies, which
        a lot shared between companies can have.
        """
        layers = self.env["stock.valuation.layer"].sudo()
        # Layers of a lot valuated product carry the lot themselves, the other
        # ones are only reachable through the lots of their stock move. The two
        # searches are disjoint thanks to the lot_id domain of the second one.
        lot_layers = layers.search([("lot_id", "in", self.ids)])
        for lot, layers_to_align in lot_layers.grouped("lot_id").items():
            layers_to_align.removal_date = lot.removal_date
        moves = (
            self.env["stock.move.line"]
            .search([("lot_id", "in", self.ids), ("quantity", "!=", 0)])
            .move_id
        )
        if not moves:
            return
        move_layers = layers.search(
            [("stock_move_id", "in", moves.ids), ("lot_id", "=", False)]
        )
        grouping = move_layers.grouped(
            lambda layer: layer.stock_move_id._get_removal_date()
        )
        for removal_date, layers_to_align in grouping.items():
            layers_to_align.removal_date = removal_date
