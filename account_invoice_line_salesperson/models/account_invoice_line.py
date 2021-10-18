# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    user_id = fields.Many2one(
        "res.users",
        "Sales Person",
        index=True,
        readonly=True,
        compute="_compute_user_id",
    )

    @api.model
    def _compute_user_id(self):
        if not self.origin:
            self.user_id = self.create_uid
            return
        else:
            i = 0
            while i < 1:
                for line in self:
                    if line.sale_line_ids:
                        for sol in line.sale_line_ids:
                            so_user_id = sol.order_id.user_id
                            line.user_id = so_user_id
                            i += 1
