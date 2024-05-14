# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    default_instruction = fields.Text(
        "Default Instructions",
        help="Default instructions to show in batch picking.",
    )
