# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("commitment_date")
    def onchange_commitment_date(self):
        if self.commitment_date and self.pricelist_id and self.partner_id:
            for line in self.order_line:
                product = line.product_id.with_context(
                    lang=self.partner_id.lang,
                    partner=self.partner_id,
                    quantity=line.product_uom_qty,
                    date=self.date_order,
                    pricelist=self.pricelist_id.id,
                    uom=line.product_uom.id,
                    fiscal_position=self.env.context.get("fiscal_position"),
                    commitment_date=self.commitment_date,
                )
                line.price_unit = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    line._get_display_price(product),
                    product.taxes_id,
                    line.tax_id,
                    line.company_id,
                )
                factor = line.secondary_uom_id.factor * line.product_uom.factor
                line.secondary_uom_price = line.price_unit * factor
