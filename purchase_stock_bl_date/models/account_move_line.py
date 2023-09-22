# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def _update_check(self):
        # force skipping to check the posted move for changing
        # accounting date from _update_valuation
        if self.env.context.get("skip_check_update"):
            return True
        return super()._update_check()
