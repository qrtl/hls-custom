# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    secondary_uom_price = fields.Float(
        "Secondary Unit Price", digits=dp.get_precision("Product Price")
    )

    @api.onchange("secondary_uom_id", "secondary_uom_price")
    def onchange_secondary_price(self):
        if not self.secondary_uom_id:
            self.secondary_uom_price = 0
            return
        if self.secondary_uom_price:
            factor = self.secondary_uom_id.factor * self.uom_id.factor
            self.price_unit = self.secondary_uom_price / factor

    @api.onchange("price_unit", "secondary_uom_id")
    def onchange_price_unit(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.uom_id.factor
        self.secondary_uom_price = self.price_unit * factor

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        """extending the standard method to always respect the pricing
        based on the secondary unit price if it is set.
        i.e. standard method recomputes unit price irrespective of
        secondary unit price, so we need to override it.
        """
        super(AccountInvoiceLine, self)._onchange_uom_id()
        self.onchange_secondary_price()

    @api.constrains("secondary_uom_id", "secondary_uom_price")
    def _check_secondary_uom_id(self):
        for line in self:
            if not line.secondary_uom_id and line.secondary_uom_price != 0.0:
                raise ValidationError(
                    _("Please enter secondary UoM or remove the secondary UoM price.")
                )
