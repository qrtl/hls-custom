# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delivery_lead = fields.Float(
        'Delivery Lead Time',
        default=0.0,
        help="Delivery lead time in number of days. "
             "Used in proposal of Delivery Due Date in deliveries.",
        )
