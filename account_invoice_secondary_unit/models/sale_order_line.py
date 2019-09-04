# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.secondary_uom_id:
            res['secondary_uom_qty'] = self._get_secondary_uom_qty(qty)
            res['secondary_uom_id'] = self.secondary_uom_id.id
        return res

    @api.multi
    def _get_secondary_uom_qty(self, qty):
        self.ensure_one()
        factor = self.secondary_uom_id.factor * \
            self.product_uom.factor
        rounding_factor = self.secondary_uom_id.uom_id.factor
        return float_round(
            qty / (factor or 1.0),
            precision_rounding=rounding_factor
        )
