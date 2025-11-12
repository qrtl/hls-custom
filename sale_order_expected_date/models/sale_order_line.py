# Copyright 2020 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta
from pytz import UTC, timezone

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        tz = self.env.user.tz
        if self.order_id.dispatch_expected_date:
            expect_datetime = fields.Datetime.from_string(
                self.order_id.dispatch_expected_date
            )
            expect_datetime = expect_datetime + relativedelta(hours=12)
            date_planned = fields.Datetime.to_string(
                timezone(tz).localize(expect_datetime).astimezone(UTC)
            )
            values.update({"date_planned": date_planned})
        return values
