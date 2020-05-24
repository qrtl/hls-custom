# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    removal_date = fields.Date("Removal Date")

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for ml in self:
            if ml.picking_id.picking_type_code == "incoming" and ml.removal_date:
                removal_date = ml.removal_date + relativedelta(hours=3)
                removal_date = fields.Datetime.context_timestamp(self, removal_date)
                ml.lot_id.write({"removal_date": removal_date})
        return res
