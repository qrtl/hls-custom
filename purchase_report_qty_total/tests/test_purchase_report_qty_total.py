# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestPurchaseReportQtyTotal(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_kg = cls.env["product.product"].create(
            {"name": "Product KG", "uom_id": cls.uom_kg.id}
        )
        cls.product_unit = cls.env["product.product"].create(
            {"name": "Product Unit", "uom_id": cls.uom_unit.id}
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].create(
            {
                "name": "Box",
                "uom_id": cls.uom_unit.id,
                "factor": 5.0,
                "product_tmpl_id": cls.product_kg.product_tmpl_id.id,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test Vendor"})

    def _create_order(self, lines):
        return self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [Command.create(vals) for vals in lines],
            }
        )

    def test_primary_totals_grouped_by_uom(self):
        order = self._create_order(
            [
                {"product_id": self.product_kg.id, "product_qty": 10.0},
                {"product_id": self.product_kg.id, "product_qty": 5.0},
                {"product_id": self.product_unit.id, "product_qty": 3.0},
            ],
        )
        totals = order.get_qty_totals()
        self.assertEqual(totals._name, "purchase.order.qty.total")
        self.assertEqual(len(totals), 2)
        kg_total = totals.filtered(lambda r: r.uom_id == self.uom_kg)
        unit_total = totals.filtered(lambda r: r.uom_id == self.uom_unit)
        self.assertEqual(kg_total.qty, 15.0)
        self.assertEqual(unit_total.qty, 3.0)

    def test_secondary_totals_paired_with_primary(self):
        order = self._create_order(
            [
                {
                    "product_id": self.product_kg.id,
                    "product_qty": 10.0,
                    "secondary_uom_id": self.secondary_unit.id,
                    "secondary_uom_qty": 2.0,
                },
                {
                    "product_id": self.product_kg.id,
                    "product_qty": 5.0,
                    "secondary_uom_id": self.secondary_unit.id,
                    "secondary_uom_qty": 1.0,
                },
            ],
        )
        totals = order.get_qty_totals()
        self.assertEqual(len(totals), 1)
        kg_total = totals.filtered(lambda r: r.uom_id == self.uom_kg)
        self.assertEqual(kg_total.qty, 15.0)
        self.assertEqual(len(kg_total.secondary_ids), 1)
        self.assertEqual(kg_total.secondary_ids.qty, 3.0)
        self.assertEqual(kg_total.secondary_ids.uom_id, self.uom_unit)

    def test_primary_without_secondary(self):
        order = self._create_order(
            [
                {"product_id": self.product_unit.id, "product_qty": 3.0},
                {
                    "product_id": self.product_kg.id,
                    "product_qty": 10.0,
                    "secondary_uom_id": self.secondary_unit.id,
                    "secondary_uom_qty": 2.0,
                },
            ],
        )
        totals = order.get_qty_totals()
        unit_total = totals.filtered(lambda r: r.uom_id == self.uom_unit)
        kg_total = totals.filtered(lambda r: r.uom_id == self.uom_kg)
        self.assertFalse(unit_total.secondary_ids)
        self.assertEqual(len(kg_total.secondary_ids), 1)

    def test_section_lines_excluded(self):
        order = self._create_order(
            [
                {
                    "display_type": "line_section",
                    "name": "Section",
                    "product_uom": False,
                },
                {"product_id": self.product_kg.id, "product_qty": 7.0},
            ],
        )
        totals = order.get_qty_totals()
        self.assertEqual(len(totals), 1)
        self.assertEqual(totals.qty, 7.0)

    def test_no_lines_returns_empty(self):
        order = self.env["purchase.order"].create({"partner_id": self.partner.id})
        totals = order.get_qty_totals()
        self.assertFalse(totals)
