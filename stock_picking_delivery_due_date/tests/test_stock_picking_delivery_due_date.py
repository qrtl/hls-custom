# Copyright 2018-2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from odoo import fields
from odoo.tests import common


class StockPickingDeliveryDueDateCase(common.TransactionCase):
    def setUp(self):
        super(StockPickingDeliveryDueDateCase, self).setUp()
        self.product = self.env["product.product"].create(
            {"name": "Product A", "type": "product", "sale_delay": 5, "uom_id": 1}
        )
        self.partner = self.env["res.partner"].browse(self.ref("base.res_partner_3"))
        self.partner.delivery_lead = 2.0
        self.main_company = self.env.ref("base.main_company")
        self.main_company.security_lead = 0

    def test_01_commitment_date_provided(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "commitment_date": fields.Datetime.now() + timedelta(days=3),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "customer_lead": self.product.sale_delay,
                            "product_uom_qty": 5,
                        },
                    )
                ],
            }
        )
        sale_order.action_confirm()
        confirm_date = fields.Datetime.now() + timedelta(days=5)
        sale_order.write({"confirmation_date": confirm_date})
        picking = sale_order.picking_ids[0]
        self.assertEqual(
            picking.delivery_due_date,
            sale_order.commitment_date,
            msg="Wrong Deliery Due Date!",
        )
        self.assertEqual(
            picking.scheduled_date,
            sale_order.commitment_date - timedelta(days=self.partner.delivery_lead),
            msg="Wrong Scheduled Date!",
        )

    def test_02_no_commitment_date(self):
        product_delay = self.product.sale_delay
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "commitment_date": False,  # no commitment date
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "customer_lead": product_delay,
                            "product_uom_qty": 5,
                        },
                    )
                ],
            }
        )
        sale_order.company_id.security_lead = 0
        sale_order.action_confirm()
        expected_date = sale_order.confirmation_date + timedelta(days=product_delay)
        picking = sale_order.picking_ids[0]
        self.assertEqual(
            picking.delivery_due_date, expected_date, msg="Wrong Deliery Due Date!"
        )
        self.assertEqual(
            picking.scheduled_date,
            expected_date - timedelta(days=self.partner.delivery_lead),
            msg="Wrong Scheduled Date!",
        )
