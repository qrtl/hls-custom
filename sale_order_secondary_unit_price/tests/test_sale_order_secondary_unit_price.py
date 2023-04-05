# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSaleOrderSecondaryUnitPrice(TransactionCase):
    def setUp(cls):
        super(TestSaleOrderSecondaryUnitPrice, cls).setUp()
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.product_category = cls.env["product.category"].create(
            {
                "name": "Test Product category",
            }
        )
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.product = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "uom_id": cls.product_uom_unit.id,
                "categ_id": cls.product_category.id,
                "secondary_uom_ids": [
                    (
                        0,
                        0,
                        {
                            "code": "D",
                            "name": "dozen",
                            "uom_id": cls.product_uom_dozen.id,
                            "factor": 12,
                        },
                    )
                ],
            }
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].search(
            [
                ("product_tmpl_id", "=", cls.product.id),
            ],
            limit=1,
        )

    def test_secondary_unit_price(self):
        sale_line_vals = [
            (
                0,
                0,
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "product_uom": self.product_uom_unit.id,
                    "secondary_uom_id": self.secondary_unit.id,
                    "price_unit": 10.00,
                },
            )
        ]
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": sale_line_vals,
            }
        )
        sale_order.order_line.onchange_price_unit()
        self.assertEqual(sale_order.order_line.secondary_uom_price, 120)

    def test_unit_price(self):
        sale_line_vals = [
            (
                0,
                0,
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "product_uom": self.product_uom_unit.id,
                    "secondary_uom_id": self.secondary_unit.id,
                    "price_unit": 5.00,
                    "secondary_uom_price": 120.00,
                },
            )
        ]
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": sale_line_vals,
            }
        )
        sale_order.order_line.onchange_secondary_price()
        self.assertEqual(sale_order.order_line.price_unit, 10)

    def test_secondary_uom_id(self):
        with self.assertRaises(ValidationError):
            sale_order = self.env["sale.order"].create(
                {
                    "partner_id": self.partner.id,
                }
            )
            self.env["sale.order.line"].create(
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "product_uom": self.product_uom_unit.id,
                    "price_unit": 10.00,
                    "secondary_uom_price": 120.00,
                    "order_id": sale_order.id,
                },
            )
