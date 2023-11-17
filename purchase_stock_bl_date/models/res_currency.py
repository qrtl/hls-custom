# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _convert(self, from_amount, to_currency, company, date, round=True):
        bl_date = self._context.get("bl_date")
        date = bl_date or date
        return super()._convert(
            from_amount=from_amount,
            to_currency=to_currency,
            company=company,
            date=date,
            round=round,
        )
