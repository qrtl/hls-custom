# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_unit_pricelist = fields.Float(
        "Unit Price PriceList",
        digits=dp.get_precision("Product Price"),
        compute="_compute_price_unit_pricelist",
    )

    @api.depends("price_unit")
    def _compute_price_unit_pricelist(self):
        for rec in self:
            if not rec.product_uom or not rec.product_id:
                rec.price_unit_pricelist = 0.0
                return
            if rec.order_id.pricelist_id and rec.order_id.partner_id:
                product = rec.product_id.with_context(
                    lang=rec.order_id.partner_id.lang,
                    partner=rec.order_id.partner_id,
                    quantity=rec.product_uom_qty,
                    date=rec.order_id.date_order,
                    pricelist=rec.order_id.pricelist_id.id,
                    uom=rec.product_uom.id,
                    fiscal_position=self.env.context.get("fiscal_position"),
                )
                rec.price_unit_pricelist = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    rec._get_display_price(product),
                    product.taxes_id,
                    rec.tax_id,
                    rec.company_id,
                )
