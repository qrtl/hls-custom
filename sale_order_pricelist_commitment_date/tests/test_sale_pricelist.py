# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestWebsiteSaleComment(common.TransactionCase):
    def setUp(self):
        super(TestWebsiteSaleComment, self).setUp()
        partner = self.env["res.partner"].create(dict(name="George"))
        SaleOrder = self.env["sale.order"]
        self.SaleOrderLine = self.env["sale.order.line"]
        self.product_id = self.env.ref("product.product_product_1")
        self.pricelist_usd = self.env["product.pricelist"].create(
            {
                "name": "USD pricelist",
                "active": True,
                "currency_id": self.env.ref("base.USD").id,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.commitment_date = date.today() + relativedelta(days=+5)
        self.sale_order = SaleOrder.create(
            {
                "partner_id": partner.id,
                "date_order": date.today(),
                "commitment_date": self.commitment_date,
                "pricelist_id": self.pricelist_usd.id,
            }
        )

    def test_compute_price_rule(self):
        self.so_line = self.SaleOrderLine.with_context(
            commitment_date=self.commitment_date
        ).create(
            {
                "product_id": self.product_id.id,
                "product_uom_qty": 1,
                "product_uom": self.product_id.uom_id.id,
                "price_unit": self.product_id.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )
        self.assertEquals(
            self.so_line._context["commitment_date"],
            self.commitment_date,
            "In Compute Price rule the commitment date pass date through context",
        )
