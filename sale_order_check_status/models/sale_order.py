# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    all_line_checked = fields.Boolean(
        string="All Line Checked",
        compute="_compute_all_line_checked",
        store=True,
        help="Indicates that all order lines that have been checked for "
        "invoicing.",
    )

    @api.depends("order_line.line_checked")
    def _compute_all_line_checked(self):
        for order in self:
            if all([line.line_checked for line in order.order_line]):
                order.all_line_checked = True
            else:
                order.all_line_checked = False
