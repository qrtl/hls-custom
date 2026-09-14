# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestSaleOrderLineAltSecondaryUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id |= cls.env.ref("uom.group_uom")
        kg = cls.env.ref("uom.product_uom_kgm")
        unit_category = cls.env.ref("uom.product_uom_categ_unit")
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "type": "consu", "uom_id": kg.id}
        )
        alt_uom = cls.env["uom.uom"].create(
            {
                "name": "Test bundle",
                "category_id": unit_category.id,
                "uom_type": "bigger",
                "factor_inv": 2.0,
                "rounding": 1.0,
            }
        )
        secondary_unit = cls.env["product.secondary.unit"]
        cls.bag = secondary_unit.create(
            {
                "name": "Bag",
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "factor": 10.0,
            }
        )
        cls.bundle = secondary_unit.create(
            {
                "name": "Bundle",
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "uom_id": alt_uom.id,
                "factor": 5.0,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {"partner_id": cls.env["res.partner"].create({"name": "Test"}).id}
        )

    def _line_vals(self, **kwargs):
        vals = {
            "order_id": self.order.id,
            "product_id": self.product.id,
            "secondary_uom_id": self.bag.id,
            "alt_secondary_uom_id": self.bundle.id,
        }
        vals.update(kwargs)
        return vals

    def test_onchange_alt_secondary_qty(self):
        """Entering the alternative quantity updates the line before saving."""
        with Form(self.order) as order_form:
            with order_form.order_line.new() as line_form:
                line_form.product_id = self.product
                line_form.secondary_uom_id = self.bag
                line_form.alt_secondary_uom_id = self.bundle
                line_form.alt_secondary_qty = 4.0
                self.assertEqual(line_form.product_uom_qty, 20.0)
                self.assertEqual(line_form.secondary_uom_qty, 2.0)
                self.assertEqual(line_form.alt_secondary_qty, 4.0)

    def test_onchange_keeps_entered_alt_secondary_qty(self):
        """A quantity that its own unit cannot represent must be kept as entered."""
        with Form(self.order) as order_form:
            with order_form.order_line.new() as line_form:
                line_form.product_id = self.product
                line_form.secondary_uom_id = self.bag
                line_form.alt_secondary_uom_id = self.bundle
                line_form.alt_secondary_qty = 4.5
                self.assertEqual(line_form.alt_secondary_qty, 4.5)
                self.assertEqual(line_form.product_uom_qty, 22.5)

    def test_create_alt_secondary_qty(self):
        """Creating a line from the alternative quantity keeps every field in sync."""
        line = self.env["sale.order.line"].create(
            self._line_vals(product_uom_qty=1.0, alt_secondary_qty=4.0)
        )
        self.assertEqual(line.product_uom_qty, 20.0)
        self.assertEqual(line.secondary_uom_qty, 2.0)

    def test_write_alt_secondary_qty(self):
        """Writing the alternative quantity updates the line quantities."""
        line = self.env["sale.order.line"].create(self._line_vals(product_uom_qty=10.0))
        line.write({"alt_secondary_qty": 4.0})
        self.assertEqual(line.product_uom_qty, 20.0)
        self.assertEqual(line.secondary_uom_qty, 2.0)

    def test_alt_secondary_qty_follows_quantity(self):
        """The alternative quantity is recomputed from the line quantity."""
        line = self.env["sale.order.line"].create(self._line_vals(product_uom_qty=10.0))
        self.assertEqual(line.alt_secondary_qty, 2.0)
        line.write({"secondary_uom_qty": 5.0})
        self.assertEqual(line.product_uom_qty, 50.0)
        self.assertEqual(line.alt_secondary_qty, 10.0)
