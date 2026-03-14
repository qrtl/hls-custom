# Copyright 2020 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import Command, fields
from odoo.tests import common


class SaleOrderDispatchDate(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def create_sale_order(self):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                        }
                    )
                ],
            }
        )

    def test_sale_order_expected_date(self):
        sale_order = self.create_sale_order()
        sale_order.action_confirm()
        self.assertEqual(
            (sale_order.picking_ids.scheduled_date).date(),
            fields.Date.context_today(sale_order),
        )
        sale_order = self.create_sale_order()
        sale_order.dispatch_expected_date = date(2025, 11, 25)
        sale_order.action_confirm()
        self.assertEqual(
            (sale_order.picking_ids.scheduled_date).date(), date(2025, 11, 25)
        )
