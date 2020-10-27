# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderLineCustomerReference(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "service"}
        )
        cls.test_partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.sale_order = cls.env["sale.order"].create(
            {"partner_id": cls.test_partner.id}
        )
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.test_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            }
        )

    def test_01_prepare_invoice_line(self):
        self.order_line.write({"client_order_ref": "Test1111"})
        self.sale_order.action_confirm()
        invoice = self.env["account.invoice"].browse(
            self.sale_order.action_invoice_create()
        )
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda i: i.product_id == self.test_product
        )
        self.assertEquals(
            invoice_line.client_order_ref, self.order_line.client_order_ref
        )
