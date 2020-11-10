# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_time = fields.Char("Delivery Time", size=9)

    def _get_shipping_address(self):
        return "{}{}{}{}".format(
            self.state_id and self.state_id.name or "",
            self.city or "",
            self.street or "",
            self.street2 or "",
        )
