# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    date_actual = fields.Date(
        'Actual Date',
        help="Used to indicate the date on which the shipment was actually "
             "done. Manually adjust the date for completed deliveries as "
             "necessary. This date is used to find target deliveries in "
             "invoice print.",
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        readonly=True,
    )

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()
        self.write({'date_actual': fields.Date.context_today(self)})
        return res
