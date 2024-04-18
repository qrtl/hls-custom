# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_unit_pricelist = fields.Float(
        "Unit Price PriceList",
        digits=dp.get_precision("Product Price"),
        compute="_compute_price_unit_pricelist",
        store=True,
    )

    @api.depends(
        "product_id",
        "product_uom",
        "product_uom_qty",
        "order_id.partner_id",
        "order_id.date_order",
        "order_id.commitment_date",
        "order_id.pricelist_id",
        "order_id.pricelist_id.item_ids",
    )
    def _compute_price_unit_pricelist(self):
        lines = self.filtered(lambda x: x.state != "cancel" and x.qty_invoiced == 0.0)
        for rec in lines:
            order = rec.order_id
            if (
                not rec.product_uom
                or not rec.product_id
                or not order.pricelist_id
                or not order.partner_id
            ):
                rec.price_unit_pricelist = 0.0
                continue
            product = rec.product_id.with_context(
                lang=order.partner_id.lang,
                partner=order.partner_id,
                quantity=rec.product_uom_qty,
                date=order.commitment_date or order.date_order,
                pricelist=order.pricelist_id.id,
                uom=rec.product_uom.id,
            )
            rec.price_unit_pricelist = self.env[
                "account.tax"
            ]._fix_tax_included_price_company(
                rec._get_display_price(product),
                product.taxes_id,
                rec.tax_id,
                rec.company_id,
            )
