# Copyright 2024 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_due_date(self):
        self.ensure_one()
        return self.commitment_date or self.expected_date
