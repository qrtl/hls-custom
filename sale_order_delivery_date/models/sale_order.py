# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_expected_date = fields.Date("Expected Delivery Date")

    def _get_due_date(self):
        self.ensure_one()
        return self.commitment_date or self.expected_date
