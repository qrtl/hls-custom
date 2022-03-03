# Copyright 2020-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests.common as common


class TestStockProductionLotName(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockProductionLotName, cls).setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product A", "type": "product", "tracking": "lot"}
        )
        cls.user = cls.env["res.users"].create(
            {"name": "test", "login": "test", "email": "test@example.com"}
        )
        cls.lot_model = cls.env["stock.production.lot"]

    def test_lot_name_get(self):
        lot = self.lot_model.sudo(self.user.id).create(
            {"name": "test lot", "product_id": self.product.id}
        )
        self.assertEqual(dict(lot.name_get())[lot.id], "test lot")

        lot.write({"removal_date": "2020-07-10 12:00:00"})
        lot._compute_removal_date_string()
        self.assertEqual(dict(lot.name_get())[lot.id], "[2020/07/10] test lot")

    def test_lot_name_search(self):
        lot = self.lot_model.sudo(self.user.id).create(
            {"name": "test lot hoge", "product_id": self.product.id}
        )
        lot.write({"removal_date": "2023-05-12 12:00:00"})
        lot._compute_removal_date_string()
        args = [("product_id", "=", self.product.id)]
        lot_res = self.lot_model.name_search(
            name="2023/05/12", args=args, operator="ilike"
        )
        self.assertEqual(len(lot_res), 1)
        self.assertEqual(lot_res[0][1], "[2023/05/12] test lot hoge")
        lot_res = self.lot_model.name_search(
            name="23-05-12", args=args, operator="ilike"
        )
        self.assertEqual(len(lot_res), 1)
        self.assertEqual(lot_res[0][1], "[2023/05/12] test lot hoge")
        lot_res = self.lot_model.name_search(name="230512", args=args, operator="ilike")
        self.assertEqual(len(lot_res), 1)
        self.assertEqual(lot_res[0][1], "[2023/05/12] test lot hoge")
