from odoo.tests.common import TransactionCase


class TestAccountInvoiceLineSaleperson(TransactionCase):
    def setUp(cls):
        super(TestAccountInvoiceLineSaleperson, cls).setUp()
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.user = (
            cls.env["res.users"]
            .sudo()
            .create(
                {
                    "email": "invoiceuser@example.com",
                    "login": "invoiceuser",
                    "name": "Invoice User",
                }
            )
        )
        cls.account_type = cls.env["account.account.type"].create(
            {
                "name": "Test",
                "type": "receivable",
            }
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST",
                "user_type_id": cls.account_type.id,
                "reconcile": True,
            }
        )
        cls.product_category = cls.env["product.category"].create(
            {
                "name": "Test Product category",
            }
        )
        cls.product_sale = cls.env["product.product"].create(
            {
                "name": "Test Sale Product",
                "sale_ok": True,
                "type": "consu",
                "categ_id": cls.product_category.id,
            }
        )
        cls.invoice_sale_vals = [
            (
                0,
                0,
                {
                    "product_id": cls.product_sale.id,
                    "name": "Test Invoice Line",
                    "account_id": cls.account.id,
                    "price_unit": 500.00,
                },
            )
        ]
        cls.invoice_sale = cls.env["account.invoice"].create(
            {
                "partner_id": cls.partner.id,
                "journal_id": cls.env["account.journal"]
                .search([("type", "=", "sale")])[0]
                .id,
                "type": "out_invoice",
                "user_id": cls.user.id,
                "invoice_line_ids": cls.invoice_sale_vals,
            }
        )

    def test_saleperson_in_invoice_line(self):
        for line in self.invoice_sale.invoice_line_ids:
            self.assertEqual(self.invoice_sale.user_id.id, line.salesman_id.id)

    def test_saleperson_in_invoice_line_with_sale_line(self):
        sale_order = self.env["sale.order"].create(
            {
                "name": "Test Sale Order",
                "partner_id": self.partner.id,
                "user_id": self.user.id,
            }
        )
        so_line = self.env["sale.order.line"]
        sale_line1 = so_line.create(
            {
                "order_id": sale_order.id,
                "name": "Line 1",
                "price_unit": 200.0,
                "product_uom_qty": 1,
                "product_id": self.product_sale.id,
            }
        )
        sale_order.action_confirm()
        inv_id = sale_order.action_invoice_create()
        invoice = self.env["account.invoice"].browse(inv_id)
        invoice.action_invoice_open()
        for line in invoice.invoice_line_ids:
            self.assertEqual(sale_order.user_id, line.salesman_id)
