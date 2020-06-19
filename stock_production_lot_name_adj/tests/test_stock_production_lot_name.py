# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestStockProductionLotName(TransactionCase):
    def setUp(self):
        super(TestStockProductionLotName, self).setUp()
        self.product = self.env["product.product"].create(
            {"name": "Product A", "type": "product", "tracking": "lot"}
        )
        self.user = self.env["res.users"].create(
            {
                "name": "test",
                "login": "test",
                "email": "test@example.com",
                "tz": "Japan",
            }
        )
        self.lot_model = self.env["stock.production.lot"]

    def test_01_lot_name_get(self):
        lot = self.lot_model.sudo(self.user.id).create(
            {"name": "test lot", "product_id": self.product.id}
        )
        self.assertEqual(dict(lot.name_get())[lot.id], "test lot")

        lot.write({"removal_date": "2020-07-10 12:00:00"})
        self.assertEqual(dict(lot.name_get())[lot.id], "[2020/07/10] test lot")

        lot.write({"removal_date": "2020-07-10 18:00:00"})
        self.assertEqual(dict(lot.name_get())[lot.id], "[2020/07/11] test lot")
