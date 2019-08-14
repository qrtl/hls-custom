# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_due_date(self):
        self.ensure_one()
        return self.commitment_date or self.expected_date
