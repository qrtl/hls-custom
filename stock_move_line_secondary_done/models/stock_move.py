# Copyright 2025 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.float_utils import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self):
        moves = super()._action_done()
        move_lines = moves.mapped("move_line_ids").filtered(
            lambda l: l.secondary_uom_id
            and float_is_zero(
                l.secondary_uom_qty_done,
                precision_rounding=l.secondary_uom_id.uom_id.rounding,
            )
        )
        for line in move_lines:
            line._onchange_qty_done()
        return moves
