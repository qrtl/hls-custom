# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_removal_date(self):
        """Return the earliest removal date among the lots of the move.

        The lots are read from the move because the lot of a valuation layer is
        only set for products with lot valuation enabled.
        """
        self.ensure_one()
        return min(filter(None, self.lot_ids.mapped("removal_date")), default=False)
