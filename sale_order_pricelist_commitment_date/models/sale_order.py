# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("commitment_date")
    def onchange_commitment_date(self):
        if self.commitment_date:
            for line in self.order_line:
                line.with_context(
                    commitment_date=self.commitment_date
                ).product_id_change()
