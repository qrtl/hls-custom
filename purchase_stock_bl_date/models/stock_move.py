# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _get_price_unit(self):
        self.ensure_one()
        bl_date = self.picking_id.bl_date
        if bl_date:
            self = self.with_context(bl_date=bl_date)
        return super()._get_price_unit()

    def update_amount_journal_entry(self):
        bl_date = self.picking_id.bl_date
        if not bl_date:
            return
        # There can be multiple account moves in case a correction entry
        # has been generated.
        account_moves = self.env["account.move"].search(
            [
                ("stock_move_id", "=", self.id),
                ("state", "=", "posted"),
                ("company_id", "=", self.env.user.company_id.id),
            ]
        )
        for account_move in account_moves:
            account_move.with_context(
                bl_date=bl_date, skip_check_update=True, check_move_validity=False
            )._onchange_date()
