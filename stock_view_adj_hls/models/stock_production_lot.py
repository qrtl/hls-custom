# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.multi
    def name_get(self):
        result = []
        for lot in self:
            name = lot.name
            if lot.removal_date:
                removal_date = datetime.strptime(
                    str(lot.removal_date), DEFAULT_SERVER_DATETIME_FORMAT
                )
                name = "[" + removal_date.date().strftime("%Y/%m/%d") + "] " + lot.name
            result.append((lot.id, name))
        return result
