# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    removal_date = fields.Date("Removal Date")

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for ml in self:
            if ml.picking_id.picking_type_code == "incoming" and ml.removal_date:
                # The time part of removal_date in lot/serial should show as
                # 12:00 for users in the same timezone as the superuser.
                removal_date = fields.Datetime.to_string(
                    ml.convert_date_to_datetime(ml.removal_date, 12)
                )
                ml.lot_id.write({"removal_date": removal_date})
        return res

    def convert_date_to_datetime(self, date, hour):
        # FIXME This method should ideally be put into another module
        # dedicated to itself, adding to the Date class.
        # It is also not optimal in terms of the performance to run this for
        # every move line (should the diff be kept in the user record of the
        # superuser? - in which case adjustments for DST is not possible).
        dt = datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=hour,
        )
        utc_timestamp = pytz.utc.localize(dt, is_dst=False)
        su_tz = self.env["res.users"].browse(SUPERUSER_ID).tz or "UTC"
        su_timestamp = pytz.timezone(su_tz).localize(dt).astimezone(pytz.utc)
        # Following conditional branching is needed due to peculiar behavior
        # of how the diff is calculated depending on the timezone.
        diff = -(utc_timestamp - su_timestamp).seconds / 3600
        if su_timestamp > utc_timestamp:
            diff = (su_timestamp - utc_timestamp).seconds / 3600
        return utc_timestamp + relativedelta(hours=diff)
