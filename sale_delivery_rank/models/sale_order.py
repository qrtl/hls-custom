# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_rank = fields.Selection(
        related="partner_shipping_id.delivery_rank",
        store=True,
        readonly=True,
    )
