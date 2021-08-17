# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    remarks = fields.Char("Remarks", help="to be printed on the delivery note")
    shipment_to = fields.Char("Shipment to", help="to to be printed on the delivery note")
