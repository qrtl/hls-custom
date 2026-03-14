# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestStockSecondaryUomQty(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "uom_id": cls.uom_kg.id,
                "uom_po_id": cls.uom_kg.id,
            }
        )
        cls.stock_secondary_unit = cls.env["product.secondary.unit"].create(
            {
                "name": "box-5kg",
                "uom_id": cls.uom_unit.id,
                "factor": 5.0,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
            }
        )
        cls.product.stock_secondary_uom_id = cls.stock_secondary_unit
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def _create_invoice(self, move_type="out_invoice", quantity=10.0, product=None):
        return self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Test Line",
                            "product_id": (product or self.product).id,
                            "product_uom_id": (product or self.product).uom_id.id,
                            "quantity": quantity,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )

    def test_stock_secondary_uom_qty(self):
        """Test quantity conversion using stock secondary unit factor."""
        invoice = self._create_invoice(quantity=10.0)
        line = invoice.invoice_line_ids
        # 10 kg / 5.0 factor = 2.0 boxes
        self.assertEqual(line.stock_secondary_uom_qty, 2.0)

    def test_stock_secondary_uom_qty_different_uom(self):
        """Test conversion when line UoM differs from product UoM."""
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Test Line",
                            "product_id": self.product.id,
                            "product_uom_id": self.uom_gram.id,
                            "quantity": 5000.0,
                            "price_unit": 0.1,
                        }
                    )
                ],
            }
        )
        line = invoice.invoice_line_ids
        # 5000 g -> 5 kg / 5.0 factor = 1.0 box
        self.assertEqual(line.stock_secondary_uom_qty, 1.0)

    def test_stock_secondary_uom_qty_no_secondary_unit(self):
        """Test that qty is 0 when product has no stock secondary unit."""
        product_no_su = self.env["product.product"].create(
            {"name": "Product No SU", "uom_id": self.uom_kg.id}
        )
        invoice = self._create_invoice(product=product_no_su)
        line = invoice.invoice_line_ids
        self.assertEqual(line.stock_secondary_uom_qty, 0.0)

    def test_signed_qty_refund(self):
        """Test that signed qty is negative for credit notes."""
        refund = self._create_invoice(move_type="out_refund", quantity=10.0)
        line = refund.invoice_line_ids
        self.assertEqual(line.signed_stock_secondary_uom_qty, -2.0)
