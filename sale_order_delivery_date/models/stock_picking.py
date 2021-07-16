# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_due_date = fields.Datetime(
        "Delivery Due Date",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        help="The date the customer is expected to receive the delivery.",
    )
    # in case of return, the value is carried over from the original document
    date_delivered = fields.Date(
        "Delivered Date",
        compute="_compute_date_delivered",
        store=True,
        help="Used to indicate the date on which the delivery was actually "
        "received by customer. Manually adjust the date for completed "
        "deliveries as necessary. This date is used to find target "
        "deliveries in invoice print.",
    )

    is_customer_outgoing = fields.Boolean(
        compute="_compute_is_customer_outgoing", store=True
    )

    @api.depends("delivery_due_date")
    def _compute_date_delivered(self):
        for pick in self.filtered(lambda x: x.delivery_due_date):
            pick.date_delivered = fields.Date.to_date(
                fields.Datetime.context_timestamp(pick, pick.delivery_due_date)
            )

    @api.depends("picking_type_code", "location_dest_id")
    def _compute_is_customer_outgoing(self):
        for pick in self:
            if (
                pick.picking_type_code == "outgoing"
                and pick.location_dest_id
                and pick.location_dest_id.usage == "customer"
            ):
                pick.is_customer_outgoing = True
