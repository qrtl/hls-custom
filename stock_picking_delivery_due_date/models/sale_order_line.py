# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(
            group_id)
        self.ensure_one()
        due_date = self.order_id._get_due_date()
        date_planned = due_date - timedelta(
            days=self.order_id.partner_shipping_id.delivery_lead or 0.0
            ) - timedelta(days=self.order_id.company_id.security_lead)
        values.update({
            'date_planned': date_planned,
        })
        return values
