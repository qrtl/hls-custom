from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestStockMoveSaleInvoicePartner(TransactionCase):
    def setUp(self):
        super(TestStockMoveSaleInvoicePartner, self).setUp()
        self.advance_inv_model = self.env["sale.advance.payment.inv"]
        self.StockMove = self.env["stock.move"]
        self.Picking = self.env["stock.picking"]
        self.warehouse = self.env["stock.warehouse"].create(
            {"name": "warehouse - test", "code": "WH-TEST"}
        )

        self.product = self.env["product.template"].create(
            {
                "name": "Product - Test",
                "type": "product",
                "list_price": 100.00,
                "standard_price": 100.00,
            }
        )
        self.partner = self.env["res.partner"].create(
            {"name": "Customer - test", "company_type": "company"}
        )
        self.invoice_partner = self.env["res.partner"].create(
            {
                "name": "Invoice Customer - test",
                "type": "invoice",
                "parent_id": self.partner.id,
            }
        )
        self.invoice_partner1 = self.env["res.partner"].create(
            {"name": "Real Invoice Customer", "parent_id": self.partner.id}
        )
        self.picking_type = self.env["stock.picking.type"].search(
            [("warehouse_id", "=", self.warehouse.id), ("code", "=", "outgoing")]
        )

    def _create_sale_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "partner_shipping_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.product_variant_ids.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product.uom_id.id,
                            "price_unit": 100.00,
                        },
                    )
                ],
            }
        )
        sale_order.action_confirm()
        return sale_order

    def test_stock_move_sale_invoice_partner(self):
        order = self._create_sale_order()
        picking = self.Picking.search([("sale_id", "=", order.id)])
        picking.move_lines.write({"quantity_done": 1})
        picking.button_validate()
        move = self.StockMove.search([("picking_id", "=", picking.id)])
        self.assertEqual(self.invoice_partner, move.invoice_partner_id)

        wizard = self.advance_inv_model.create({"advance_payment_method": "delivered"})
        wizard.with_context(
            active_model="sale.order",
            active_ids=[order.id],
            active_id=order.id,
        ).create_invoices()
        invoice = order.invoice_ids
        invoice.write({"partner_id": self.invoice_partner1.id})
        self.assertEqual(move.invoice_partner_id, self.invoice_partner1)
