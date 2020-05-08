# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from itertools import chain

from odoo import api, fields, models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    @api.multi
    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        date = self._context.get(
            "commitment_date") or self._context.get("date") or fields.Date.today()
        date = fields.Date.to_date(date)
        return super(Pricelist, self)._compute_price_rule(
            products_qty_partner=products_qty_partner, date=date, uom_id=uom_id)
