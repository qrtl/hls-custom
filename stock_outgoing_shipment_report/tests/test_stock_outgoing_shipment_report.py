# Copyright 2020 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, datetime

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAccountPaymentImportSbt(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "zip": "123-4567",
                "state_id": cls.env.ref("base.state_jp_jp-02").id,
                "city": "City",
                "street": "Street",
                "street2": "Street2",
                # 16 characters to test truncation to 12
                "phone": "03-1234-5678-999",
                "delivery_time": "test",
                "ref": "CUST001",
            }
        )
        cls.env.ref("delivery.free_delivery_carrier").write({"shipping_mode": "10"})
        cls.product = cls.env["product.product"].create(
            {"name": "Product A", "default_code": "Test Code"}
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "carrier_id": cls.env.ref("delivery.free_delivery_carrier").id,
            }
        )
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
                "client_order_ref": "ref0001",
                "note": "Test Note",
            }
        )
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
                "client_order_ref": "ref0002",
            }
        )
        cls.sale_order.action_confirm()
        cls.pickings = cls.sale_order.picking_ids

    def test_partner_get_shipment_report_vals(self):
        vals = self.partner._get_shipment_report_vals()
        self.assertEqual(vals["partner_ref"], "CUST001")
        self.assertEqual(vals["partner_zip"], "123-4567")
        state_name = self.env.ref("base.state_jp_jp-02").name
        self.assertEqual(vals["partner_address"], f"{state_name}CityStreetStreet2")
        # Truncated to 12 characters
        self.assertEqual(vals["partner_phone"], "03-1234-5678")
        self.assertEqual(vals["customer_delivery_note"], "test")

    def test_generate_stock_outgoing_shipment_report(self):
        self.pickings.generate_stock_outgoing_shipment_report()
        report_lines = self.env["stock.outgoing.shipment.report"].search([])
        self.assertEqual(len(report_lines), 2)
        test_line = report_lines[0]
        self.assertEqual(test_line.shipping_mode, "10")
        self.assertEqual(
            test_line.carrier_name,
            self.env.ref("delivery.free_delivery_carrier").name[:20],
        )
        self.assertEqual(test_line.product_code, self.product.default_code[:7])
        self.assertEqual(test_line.product_name, self.product.name)
        self.assertEqual(test_line.client_order_ref, "ref0001")
        self.assertEqual(test_line.memo, "Test Note")

    def test_lot_num_constraint(self):
        report = self.env["stock.outgoing.shipment.report"].create({})
        report.lot_num = "ABC123"  # ASCII - should pass
        with self.assertRaises(ValidationError):
            report.lot_num = "あ１２３"  # Non-ASCII - should fail

    def test_compute_date_fields(self):
        move = self.pickings.move_ids[0]
        move.write(
            {
                "date": datetime(2025, 1, 15, 10, 0, 0),
                "date_deadline": datetime(2025, 1, 20, 10, 0, 0),
            }
        )
        report = self.env["stock.outgoing.shipment.report"].create(
            {
                "move_id": move.id,
                "expiry_date_edit": date(2025, 2, 28),
            }
        )
        self.assertEqual(report.dispatch_date, "2025/01/15")
        self.assertEqual(report.delivery_date, "2025/01/20")
        self.assertEqual(report.expiry_date, "2025/02/28")
