# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from odoo import fields
from odoo.tests import common
from pytz import timezone, UTC

import datetime

class SaleOrderDeliveryDate(common.TransactionCase):
    def setUp(self):
        super(SaleOrderDeliveryDate, self).setUp()
        self.product = self.env["product.product"].create(
            {"name": "Product A", "type": "product", "sale_delay": 5, "uom_id": 1}
        )
        self.partner = self.env["res.partner"].browse(self.ref("base.res_partner_3"))

    def test_01_commitment_date_provided(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "commitment_date": fields.Datetime.now() + timedelta(days=3),
                "delivery_expected_date": datetime.date.today(),
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
        today_datetime = fields.Datetime.from_string(datetime.date.today())
        scheduled_date = fields.Datetime.to_string(timezone(self.env.user.tz).localize(today_datetime).astimezone(UTC))
        sale_order.write({"confirmation_date": confirm_date})
        picking = sale_order.picking_ids[0]
        self.assertEqual(
            picking.delivery_due_date,
            sale_order.commitment_date,
            msg="Wrong Deliery Due Date!",
        )
        self.assertEqual(
            fields.Datetime.to_string(picking.scheduled_date),
            scheduled_date,
            msg="Wrong Scheduled Date!",
        )

    def test_02_no_commitment_date(self):
        product_delay = self.product.sale_delay
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "commitment_date": False,  # no commitment date
                "delivery_expected_date": datetime.date.today(),
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
        sale_order.action_confirm()
        expected_date = sale_order.confirmation_date + timedelta(days=product_delay)
        today_datetime = fields.Datetime.from_string(datetime.date.today())
        scheduled_date = fields.Datetime.to_string(timezone(self.env.user.tz).localize(today_datetime).astimezone(UTC))
        picking = sale_order.picking_ids[0]
        self.assertEqual(
            picking.delivery_due_date, expected_date, msg="Wrong Deliery Due Date!"
        )
        self.assertEqual(
            fields.Datetime.to_string(picking.scheduled_date),
            scheduled_date,
            msg="Wrong Scheduled Date!",
        )
