# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderSecondaryUnit(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.product_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product_uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.product"].create(
            {
                "name": "test",
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "unit-700",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.7,
                        },
                    )
                ],
            }
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].search(
            [
                ("product_tmpl_id", "=", cls.product.product_tmpl_id.id),
            ]
        )
        cls.product.sale_secondary_uom_id = cls.secondary_unit.id
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "test - partner",
            }
        )
        invoice_line_vals = [
            (
                0,
                0,
                {
                    "name": cls.product.name,
                    "product_id": cls.product.id,
                    "account_id": cls.account.id,
                    "uom_id": cls.product.uom_id.id,
                    "price_unit": 1000.00,
                },
            )
        ]
        cls.invoice = cls.env["account.invoice"].create(
            {
                "partner_id": cls.partner.id,
                "journal_id": cls.env["account.journal"]
                .search([("type", "=", "sale")])[0]
                .id,
                "type": "out_invoice",
                "invoice_line_ids": invoice_line_vals,
            }
        )
        cls.invoice._onchange_partner_id()

    def test_onchange_secondary_uom(self):
        self.invoice.invoice_line_ids.write(
            {
                "secondary_uom_id": self.secondary_unit.id,
                "secondary_uom_qty": 5,
            }
        )
        self.invoice.invoice_line_ids.onchange_secondary_uom()
        self.assertEqual(self.invoice.invoice_line_ids.quantity, 3.5)

    def test_onchange_secondary_unit_product_uom_qty(self):
        self.invoice.invoice_line_ids.update(
            {
                "secondary_uom_id": self.secondary_unit.id,
                "quantity": 3.5,
            }
        )
        self.invoice.invoice_line_ids.onchange_secondary_unit_product_uom_qty()
        self.assertEqual(self.invoice.invoice_line_ids.secondary_uom_qty, 5.0)

    def test_default_secondary_unit(self):
        self.invoice.invoice_line_ids._onchange_product_id()
        self.assertEqual(
            self.invoice.invoice_line_ids.secondary_uom_id, self.secondary_unit
        )

    def test_onchange_order_product_uom(self):
        self.invoice.invoice_line_ids.update(
            {
                "secondary_uom_id": self.secondary_unit.id,
                "uom_id": self.product_uom_gram.id,
                "quantity": 3500.00,
            }
        )
        self.invoice.invoice_line_ids.onchange_product_uom_for_secondary()
        self.assertEqual(self.invoice.invoice_line_ids.secondary_uom_qty, 5.0)
