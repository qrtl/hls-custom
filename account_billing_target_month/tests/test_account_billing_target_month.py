# Copyright 2026 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.tests.common import TransactionCase


class TestAccountBillingTargetMonth(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.billing = cls.env["account.billing"].create(
            {
                "partner_id": cls.partner.id,
                "threshold_date": date(2026, 3, 15),
            }
        )

    def test_target_month(self):
        self.assertEqual(self.billing.target_month, "3")
