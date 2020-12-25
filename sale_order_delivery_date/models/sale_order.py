# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dispatch_expected_date = fields.Date(
        "Expected Dispatch Date",
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        copy=False,
        readonly=True,
        default=fields.Date.context_today,
        help="The input date will be passed over to the delivery as Scheduled Date.",
    )

    def _get_due_date(self):
        self.ensure_one()
        return self.commitment_date or self.expected_date
