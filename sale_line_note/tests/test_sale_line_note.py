# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestSaleLineNote(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product A", "type": "product"}
        )
        cls.partner = cls.env.ref("base.res_partner_3")

    def test_01_delivery_note(self):
        sale_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        order_line = self.env["sale.order.line"].create(
            {
                "name": self.product.name,
                "product_id": self.product.id,
                "delivery_note": "Test Note",
                "product_uom_qty": 5,
                "order_id": sale_order.id,
            }
        )
        sale_order.action_confirm()
        move = order_line.move_ids and order_line.move_ids[0]
        self.assertEqual(
            move.note,
            "Test Note",
        )
