# Copyright 2026 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBilling(models.Model):
    _inherit = "account.billing"

    target_month = fields.Selection(
        selection=[
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        compute="_compute_target_month",
        store=True,
        readonly=False,
    )

    @api.depends("threshold_date")
    def _compute_target_month(self):
        for rec in self:
            if not rec.threshold_date:
                rec.target_month = False
                continue
            rec.target_month = str(rec.threshold_date.month)
