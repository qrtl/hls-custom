# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    bl_date = fields.Date(string="BL Date")
    force_bl_date = fields.Boolean(string="Force BL Date")

    def action_toggle_is_locked(self):
        if not self.is_locked and self.state == "done" and self.force_bl_date:
            for move in self.move_ids_without_package:
                move.write(
                    {
                        "price_unit": move._get_price_unit(),
                    }
                )
                if move.product_id.cost_method == "average":
                    move.cost_price_avco_sync()
                else:
                    move._run_valuation()
                move.update_amount_journal_entry()
        return super().action_toggle_is_locked()
