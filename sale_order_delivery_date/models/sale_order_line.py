# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from pytz import UTC, timezone


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        tz = self.env.user.tz
        expect_datetime = fields.Datetime.from_string(
            self.order_id.delivery_expected_date
        )
        date_planned = fields.Datetime.to_string(
            timezone(tz).localize(expect_datetime).astimezone(UTC)
        )
        values.update({"date_planned": date_planned})
        return values
