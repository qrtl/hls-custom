# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

FIELDS_PROPERTIES = {
    "shipping_mode": ["Char", 2],
    "carrier_name": ["Char", 20],
    "partner_ref": ["Char", 10],
    "partner_zip": ["Char", 8],
    "partner_address": ["Char", 80],
    "product_code": ["Char", 7],
    "product_name": ["Char", 32],
    "case_qty": ["Float", 5],
    "separate_qty": ["Float", 5],
    "lot_branch_num": ["Float", 2],
    "delivery_division": ["Char", 1],
    "customer_delivery_note": ["Char", 9],
    "client_order_ref": ["Char", 30],
    "memo": ["Char", 9],
}


class StockOutgoingShipmentReport(models.Model):
    _name = "stock.outgoing.shipment.report"

    move_id = fields.Many2one(
        "stock.move",
        string="Stock Move",
        readonly=True,
    )
    dispatch_date = fields.Char(
        string="Dispatch Date", compute="_compute_date_fields", store=True
    )
    delivery_date = fields.Char(
        string="Delivery Date", compute="_compute_date_fields", store=True
    )
    shipping_mode = fields.Char("Shipping Mode")
    carrier_id = fields.Many2one("delivery.carrier")
    carrier_name = fields.Char("Carrier")
    partner_name = fields.Char("Customer")
    partner_ref = fields.Char("Customer Code")
    partner_zip = fields.Char("Zip")
    partner_address = fields.Char("Address")
    partner_phone = fields.Char("Phone")
    product_code = fields.Char("Product Code")
    product_name = fields.Char("Product Name")
    case_qty = fields.Integer("Case Quantity")
    separate_qty = fields.Integer("Separate Quantity")
    expiry_date_edit = fields.Date("Expiry Date (Edit)")
    expiry_date = fields.Char(
        string="Expiry Date", compute="_compute_date_fields", store=True
    )
    lot_num = fields.Char("Warehouse Company Lot")
    lot_branch_num = fields.Char("Warehouse Company Lot Branch")
    delivery_division = fields.Char("Delivery Division")
    customer_delivery_note = fields.Char("Customer Delivery Note")
    client_order_ref = fields.Char("Customer Reference")
    reference = fields.Char("Reference")
    memo = fields.Char("Memo")
    date_created = fields.Date(
        "Created Date (Date Only)",
        default=fields.Date.context_today,
        store=True,
    )

    @api.multi
    @api.depends(
        "move_id.date_expected",
        "move_id.picking_id.delivery_due_date",
        "expiry_date_edit",
    )
    def _compute_date_fields(self):
        date_format = "%Y/%m/%d"
        for line in self:
            if line.move_id.date_expected:
                line.dispatch_date = fields.Datetime.context_timestamp(
                    self, line.move_id.date_expected
                ).strftime(date_format)
            if line.move_id.picking_id.delivery_due_date:
                line.delivery_date = fields.Datetime.context_timestamp(
                    self, line.move_id.picking_id.delivery_due_date
                ).strftime(date_format)
            if line.expiry_date_edit:
                line.expiry_date = line.expiry_date_edit.strftime(date_format)

    @api.constrains(
        "shipping_mode",
        "carrier_name",
        "partner_ref",
        "partner_zip",
        "partner_address",
        "product_code",
        "product_name",
        "case_qty",
        "separate_qty",
        "lot_branch_num",
        "delivery_division",
        "customer_delivery_note",
        "client_order_ref",
        "memo",
    )
    def _validate_field_length(self):
        msg = _("%s should be at most %s digit(s).")
        for rec in self:
            for field, prop in FIELDS_PROPERTIES.items():
                if rec[field] and len(str(rec[field])) > prop[1]:
                    raise ValidationError(
                        msg % (_(rec.fields_get(field)[field].get("string")), prop[1])
                    )

    @api.constrains("case_qty", "separate_qty", "lot_branch_num")
    def _validate_number_fields(self):
        msg = _("Only numbers are allowed for %s field.")
        for rec in self:
            for field, prop in FIELDS_PROPERTIES.items():
                if prop[0] == "Float":
                    try:
                        int(rec[field])
                    except Exception:
                        try:
                            float(rec[field])
                        except Exception:
                            raise ValidationError(
                                msg % _(rec.fields_get(field)[field].get("string"))
                            )

    @api.constrains("lot_num")
    def _check_lot_num(self):
        for rec in self:
            if not rec.lot_num:
                return
            try:
                rec.lot_num.encode("ascii")
            except UnicodeEncodeError:
                raise ValidationError(
                    _("Please key in the warehouse lot in ASCII characters.")
                )
