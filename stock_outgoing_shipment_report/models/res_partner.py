# Copyright 2020 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_time = fields.Char(size=9)

    def _get_shipping_address(self):
        return "{}{}{}{}".format(
            self.state_id and self.state_id.name or "",
            self.city or "",
            self.street or "",
            self.street2 or "",
        )

    def _get_shipment_report_vals(self):
        partner_address = self._get_shipping_address()
        return {
            "partner_ref": self.ref[:10] if self.ref else False,
            "partner_zip": self.zip[:8] if self.zip else False,
            "partner_name": self.display_name,
            "partner_address": partner_address[:80] if partner_address else False,
            "partner_phone": self.phone[:12] if self.phone else False,
            "customer_delivery_note": self.delivery_time,
        }
