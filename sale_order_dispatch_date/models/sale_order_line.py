# Copyright 2020 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from pytz import UTC, timezone

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        if self.order_id.dispatch_expected_date:
            user_tz = timezone(self.env.user.tz or "UTC")
            local_date = self.order_id.dispatch_expected_date
            local_dt = user_tz.localize(datetime.combine(local_date, time(12, 0)))
            utc_dt = local_dt.astimezone(UTC).replace(tzinfo=None)
            values["date_planned"] = fields.Datetime.to_string(utc_dt)
        return values
