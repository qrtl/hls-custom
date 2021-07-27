# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_partner_vals(self, partner):
        partner_address = partner._get_shipping_address()
        return {
            "partner_ref": partner.ref[:10] if partner.ref else False,
            "partner_zip": partner.zip[:8] if partner.zip else False,
            "partner_name": partner.display_name,
            "partner_address": partner_address[:80] if partner_address else False,
            "partner_phone": partner.phone[:12] if partner.phone else False,
            "customer_delivery_note": partner.delivery_time,
        }

    @api.multi
    def generate_stock_outgoing_shipment_report(self):
        report_obj = self.env["stock.outgoing.shipment.report"]
        moves = self.mapped("move_lines")
        for move in moves:
            order = move.group_id.sale_id
            partner = move.picking_partner_id
            product = move.product_id
            vals = {
                "move_id": move.id,
                "shipping_mode": order.carrier_id.shipping_mode,
                "carrier_id": order.carrier_id.id if order else False,
                "carrier_name": order.carrier_id.name[:20]
                if order and order.carrier_id else False,
                "product_code": product.default_code[:7]
                if product and product.default_code else False,
                "product_name": product.name[:32],
                "client_order_ref": move.sale_line_id
                and move.sale_line_id.client_order_ref,
                "memo": move.note[:9] if move.note else False,
            }
            secondary_uom = move.product_id.stock_secondary_uom_id
            if secondary_uom:
                factor = secondary_uom.factor * move.product_uom.factor
                vals.update(
                    {
                        "case_qty": int(
                            (move.quantity_done or move.reserved_availability)
                            / (factor or 1.0)
                        )
                    }
                )
            if partner:
                partner_vals = self._get_partner_vals(partner)
                vals.update(partner_vals)
            move_rec = report_obj.search([("move_id", "=", move.id)])
            move_rec.write(vals) if move_rec else report_obj.create(vals)
        return self.env.ref(
            "stock_outgoing_shipment_report.action_stock_outgoing_shipment_report"
        ).read()[0]
