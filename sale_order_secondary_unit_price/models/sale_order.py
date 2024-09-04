# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("commitment_date")
    def onchange_commitment_date(self):
        super().onchange_commitment_date()
        if self.commitment_date and self.pricelist_id and self.partner_id:
            for line in self.order_line:
                factor = line.secondary_uom_id.factor * line.product_uom.factor
                line.secondary_uom_price = line.price_unit * factor
