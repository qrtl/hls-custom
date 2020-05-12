# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from odoo.tests import common, tagged
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


@tagged("post_install", "-at_install")
class TestWebsiteSaleComment(common.TransactionCase):
    def setUp(self):
        super(TestWebsiteSaleComment, self).setUp()
        partner = self.env["res.partner"].create(dict(name="George"))
        SaleOrder = self.env["sale.order"]
        self.SaleOrderLine = self.env["sale.order.line"]
        self.product_id = self.env.ref("product.product_product_1")
        self.product_id.write({"lst_price": 10})
        today = date.today()
        next_week = today + timedelta(weeks=1)

        self.pricelist_usd = self.env["product.pricelist"].create(
            {
                "name": "USD pricelist",
                "active": True,
                "currency_id": self.env.ref("base.USD").id,
                "company_id": self.env.user.company_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "date_start": today.strftime(DEFAULT_SERVER_DATE_FORMAT),
                            "date_end": next_week.strftime(DEFAULT_SERVER_DATE_FORMAT),
                        },
                    )
                ],
            }
        )
        self.commitment_date = date.today() + relativedelta(days=+5)
        self.sale_order = SaleOrder.create(
            {"partner_id": partner.id, "date_order": date.today()}
        )

    def test_compute_price_rule(self):
        """
            This function will check the commitment date is passed correctly or not.
        """
        self.sale_order.write(
            {
                "commitment_date": self.commitment_date,
                "pricelist_id": self.pricelist_usd.id,
            }
        )
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
        self.sale_order.onchange_commitment_date()
        self.assertEquals(
            self.so_line._context["commitment_date"],
            self.commitment_date,
            "In Compute Price rule the commitment date pass date through context",
        )
        self.assertEquals(
            self.so_line.price_unit,
            100,
            "It compare the price unit with fixed price in price list.",
        )

    def test_onchange_commitment_date(self):
        """
            This function will check the price unit based
             on price list and commitment date.
        """
        self.so_line = self.SaleOrderLine.create(
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
            self.so_line.price_unit,
            self.product_id.list_price,
            "It will check with original product price"
            " unit and compare with product list price",
        )
        self.commitment_date = date.today() + relativedelta(days=+3)
        self.sale_order.write(
            {
                "pricelist_id": self.pricelist_usd.id,
                "commitment_date": self.commitment_date,
            }
        )
        self.sale_order.onchange_commitment_date()
        self.assertEquals(
            self.so_line.price_unit,
            100,
            "It compare the price unit with fixed price in price list.",
        )
