# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def generate_stock_outgoing_shipment_report(self):
        moves = self.mapped("move_lines")
        self._cr.execute("DELETE FROM stock_outgoing_shipment_report")
        for move in moves:
            order = move.group_id.sale_id
            partner = move.picking_partner_id
            product = move.product_id
            partner_address = partner._get_shipping_address()
            vals = {
                "move_id": move.id,
                "shipping_mode": order.carrier_id.shipping_mode,
                "carrier_name": order.carrier_id.name[:20]
                if order and order.carrier_id and len(order.carrier_id.name) > 20
                else order and order.carrier_id and order.carrier_id.name or False,
                "product_code": product.default_code[:7]
                if product and product.default_code and len(product.default_code) > 7
                else product and product.default_code,
                "product_name": product.name[:32]
                if product and len(product.name) > 32
                else product and product.name,
                "case_qty": int(move.secondary_uom_qty) or False,
                "client_order_ref": move.sale_line_id
                and move.sale_line_id.client_order_ref,
            }
            if partner:
                vals.update(
                    {
                        "partner_ref": partner.ref[:10]
                        if partner.ref and len(partner.ref) > 10
                        else partner.ref,
                        "partner_zip": partner.zip[:8]
                        if partner.zip and len(partner.zip) > 8
                        else partner.zip,
                        "partner_name": partner.display_name[:32]
                        if len(partner.display_name) > 32
                        else partner.display_name,
                        "partner_address": partner_address[:80]
                        if len(partner_address) > 80
                        else partner_address,
                        "partner_phone": partner.phone[:12]
                        if partner.phone and len(partner.phone) > 12
                        else partner and partner.phone,
                        "customer_delivery_note": partner.delivery_time,
                    }
                )
            self.env["stock.outgoing.shipment.report"].create(vals)
        return self.env.ref(
            "stock_outgoing_shipment_report.action_stock_outgoing_shipment_report"
        ).read()[0]
