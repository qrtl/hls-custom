# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.multi
    def name_get(self):
        result = []
        for lot in self:
            name = lot.name
            if lot.removal_date:
                # Convert removal_date to user's timezone. The design decision
                # here is to use user's timezone, instead of superuser's.
                removal_date = fields.Datetime.context_timestamp(self, lot.removal_date)
                name = "[" + removal_date.date().strftime("%Y/%m/%d") + "] " + lot.name
            result.append((lot.id, name))
        return result
