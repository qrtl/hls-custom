# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_show_purchase_shipping_address = fields.Boolean(
        "Show Purchase Shipping Address",
        implied_group="purchase_report_custom_hls.group_show_purchase_shipping_address",
    )
