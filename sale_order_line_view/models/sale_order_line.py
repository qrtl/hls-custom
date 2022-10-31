# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        related="order_id.date_order",
        string="Order Date",
        readonly=True,
        store=True,
    )
    commitment_date = fields.Datetime(
        related="order_id.commitment_date",
        string="Commitment Date",
        readonly=True,
        store=True,
    )
    state = fields.Selection(
        related="order_id.state",
        string="Status",
        readonly=True,
        store=True,
    )
    partner_shipping_id = fields.Many2one(
        related="order_id.partner_shipping_id",
        string="Delivery Address",
        readonly=True,
        store=True,
    )
    partner_invoice_id = fields.Many2one(
        related="order_id.partner_invoice_id",
        string="Invoice Address",
        readonly=True,
        store=True,
    )
    line_checked = fields.Boolean(
        string="Checked",
        compute="_compute_line_checked",
        readonly=False,
        store=True,
        help="Select to indicate that the line is ready for invoicing.",
    )

    @api.multi
    # 'qty_invoiced' does not need to be a trigger
    @api.depends(
        "qty_delivered", "product_uom_qty", "price_unit", "secondary_uom_price"
    )
    def _compute_line_checked(self):
        for line in self:
            line.line_checked = False
