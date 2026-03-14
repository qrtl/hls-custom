# Copyright 2020 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockOutgoingShipmentReport(models.Model):
    _name = "stock.outgoing.shipment.report"
    _description = "Stock Outgoing Shipment Report"

    move_id = fields.Many2one(
        "stock.move",
        string="Stock Move",
        readonly=True,
    )
    dispatch_date = fields.Char(compute="_compute_date_fields", store=True)
    delivery_date = fields.Char(compute="_compute_date_fields", store=True)
    shipping_mode = fields.Char(size=2)
    carrier_id = fields.Many2one("delivery.carrier")
    carrier_name = fields.Char("Carrier", size=20)
    partner_name = fields.Char("Customer")
    partner_ref = fields.Char("Customer Code", size=10)
    partner_zip = fields.Char("Zip", size=8)
    partner_address = fields.Char("Address", size=80)
    partner_phone = fields.Char("Phone")
    product_code = fields.Char(size=7)
    product_name = fields.Char(size=32)
    case_qty = fields.Integer("Case Quantity")
    separate_qty = fields.Integer("Separate Quantity")
    expiry_date_edit = fields.Date("Expiry Date (Edit)")
    expiry_date = fields.Char(compute="_compute_date_fields", store=True)
    lot_num = fields.Char("Warehouse Company Lot")
    lot_branch_num = fields.Char("Warehouse Company Lot Branch", size=2)
    delivery_division = fields.Char(size=1)
    customer_delivery_note = fields.Char(size=9)
    client_order_ref = fields.Char("Customer Reference", size=30)
    reference = fields.Char()
    memo = fields.Char(size=9)
    date_created = fields.Date(
        "Created Date (Date Only)",
        default=fields.Date.context_today,
        store=True,
    )

    @api.depends("move_id.date", "move_id.date_deadline", "expiry_date_edit")
    def _compute_date_fields(self):
        date_format = "%Y/%m/%d"
        for line in self:
            move = line.move_id
            if move.date:
                line.dispatch_date = fields.Datetime.context_timestamp(
                    self, move.date
                ).strftime(date_format)
            if move.date_deadline:
                line.delivery_date = fields.Datetime.context_timestamp(
                    self, move.date_deadline
                ).strftime(date_format)
            if line.expiry_date_edit:
                line.expiry_date = line.expiry_date_edit.strftime(date_format)

    @api.constrains("lot_num")
    def _check_lot_num(self):
        for rec in self:
            if rec.lot_num and not rec.lot_num.isascii():
                raise ValidationError(
                    _("Please key in the warehouse lot in ASCII characters.")
                )
