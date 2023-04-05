# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAccountInvoiceSecondaryUnitPrice(TransactionCase):
    def setUp(cls):
        super(TestAccountInvoiceSecondaryUnitPrice, cls).setUp()
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.account_type = cls.env["account.account.type"].create(
            {
                "name": "Test",
                "type": "receivable",
            }
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST",
                "user_type_id": cls.account_type.id,
                "reconcile": True,
            }
        )
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
        invoice_line_vals = [
            (
                0,
                0,
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "account_id": self.account.id,
                    "uom_id": self.product_uom_unit.id,
                    "secondary_uom_id": self.secondary_unit.id,
                    "price_unit": 10.00,
                },
            )
        ]
        invoice = self.env["account.invoice"].create(
            {
                "partner_id": self.partner.id,
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")])[0]
                .id,
                "type": "out_invoice",
                "invoice_line_ids": invoice_line_vals,
            }
        )
        invoice.invoice_line_ids.onchange_price_unit()
        self.assertEqual(invoice.invoice_line_ids.secondary_uom_price, 120)

    def test_unit_price(self):
        invoice_line_vals = [
            (
                0,
                0,
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "account_id": self.account.id,
                    "uom_id": self.product_uom_unit.id,
                    "secondary_uom_id": self.secondary_unit.id,
                    "price_unit": 5.00,
                    "secondary_uom_price": 120.00,
                },
            )
        ]
        invoice = self.env["account.invoice"].create(
            {
                "partner_id": self.partner.id,
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")])[0]
                .id,
                "type": "out_invoice",
                "invoice_line_ids": invoice_line_vals,
            }
        )
        invoice.invoice_line_ids.onchange_secondary_price()
        self.assertEqual(invoice.invoice_line_ids.price_unit, 10)

    def test_secondary_uom_id(self):
        with self.assertRaises(ValidationError):
            self.env["account.invoice.line"].create(
                {
                    "product_id": self.product.product_variant_id.id,
                    "name": "Test Invoice Line",
                    "account_id": self.account.id,
                    "uom_id": self.product_uom_unit.id,
                    "price_unit": 10.00,
                    "secondary_uom_price": 120.00,
                },
            )
