# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import common


class TestStockMove(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.supplier_location = cls.env.ref("stock.stock_location_suppliers")
        cls.productA = cls.env["product.product"].create(
            {
                "name": "Product A",
                "is_storable": True,
                "tracking": "serial",
                "categ_id": cls.env.ref("product.product_category_all").id,
                "use_expiration_date": True,
            }
        )

    def test_lot_display_name_and_search(self):
        lot = self.env["stock.lot"].create(
            {
                "name": "test lot",
                "product_id": self.productA.id,
                "removal_date": "2025-12-12 12:00:00",
            }
        )
        self.assertEqual(lot.display_name, "[2025/12/12] test lot")
        args = [("product_id", "=", self.productA.id)]
        lot_res = self.env["stock.lot"].name_search(
            name="2025/12/12", args=args, operator="ilike"
        )
        self.assertEqual(len(lot_res), 1)
        self.assertEqual(lot_res[0][1], "[2025/12/12] test lot")
        lot_res = self.env["stock.lot"].name_search(
            name="25-12-12", args=args, operator="ilike"
        )
        self.assertEqual(len(lot_res), 1)
        self.assertEqual(lot_res[0][1], "[2025/12/12] test lot")
