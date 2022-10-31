# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import SUPERUSER_ID
from odoo.tests import common


class TestStockMove(common.TransactionCase):
    def setUp(self):
        super(TestStockMove, self).setUp()
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.supplier_location = self.env.ref("stock.stock_location_suppliers")
        self.partner_delta_id = self.env.ref("base.res_partner_4")
        self.picking_type_in = self.ref("stock.picking_type_in")

        self.picking_id = self.env["stock.picking"].create(
            {
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
                "partner_id": self.partner_delta_id.id,
                "picking_type_id": self.picking_type_in,
            }
        )
        self.productA = self.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
                "tracking": "serial",
                "categ_id": self.env.ref("product.product_category_all").id,
            }
        )

    def test_action_done(self):
        """This test perform to evaluate the action_done method
        which converts removal date to a datetime according to
        superuser's timezone."""

        # Adding UTC timezone for SUPERUSER.
        self.env["res.users"].browse(SUPERUSER_ID).write({"tz": "UTC"})

        # Move creation
        move1 = self.env["stock.move"].create(
            {
                "name": "test_in_1",
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
                "product_id": self.productA.id,
                "product_uom": self.productA.uom_id.id,
                "product_uom_qty": 2.0,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
            }
        )
        # Confirm and assign move
        move1._action_confirm()
        move1._action_assign()

        # First Move time is based on UTC
        move_line_1 = move1.move_line_ids[0]
        move_line_1.lot_name = "sn111"
        move_line_1.qty_done = 1
        move_line_1.removal_date = "2020-01-01"

        # First Move line Done
        move_line_1._action_done()
        self.assertEqual(str(move_line_1.lot_id.removal_date), "2020-01-01 12:00:00")

        # Adding Japan timezone for SUPERUSER.
        self.env["res.users"].browse(SUPERUSER_ID).write({"tz": "Japan"})

        # Second Move time is based on Japan
        move_line_2 = move1.move_line_ids[1]
        move_line_2.lot_name = "sn3"
        move_line_2.qty_done = 1
        move_line_2.removal_date = "2020-01-01"

        # Second Move line Done
        move_line_2._action_done()
        self.assertEqual(str(move_line_2.lot_id.removal_date), "2020-01-01 03:00:00")
