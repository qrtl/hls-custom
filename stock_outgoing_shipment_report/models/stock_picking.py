# Copyright 2021 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def generate_stock_outgoing_shipment_report(self):
        report_obj = self.env["stock.outgoing.shipment.report"]
        moves = self.mapped("move_ids")
        for move in moves:
            carrier = move.picking_id.carrier_id
            partner = move.picking_id.partner_id
            product = move.product_id
            sale_line = move.sale_line_id
            vals = {
                "move_id": move.id,
                "shipping_mode": carrier.shipping_mode,
                "carrier_id": carrier.id,
                "carrier_name": carrier and carrier.name[:20] or False,
                "product_code": product.default_code[:7]
                if product.default_code
                else False,
                "product_name": product.name[:32],
                "client_order_ref": sale_line.client_order_ref,
                "memo": sale_line.note[:9] if sale_line.note else False,
            }
            secondary_uom = (
                product.stock_secondary_uom_id
                or move.product_tmpl_id.stock_secondary_uom_id
            )
            if secondary_uom:
                factor = secondary_uom.factor * move.product_uom.factor
                vals.update({"case_qty": int(move.quantity / (factor or 1.0))})
            if partner:
                partner_vals = partner._get_shipment_report_vals()
                vals.update(partner_vals)
            move_rec = report_obj.search([("move_id", "=", move.id)])
            move_rec.write(vals) if move_rec else report_obj.create(vals)
        return self.env["ir.actions.act_window"]._for_xml_id(
            "stock_outgoing_shipment_report.action_stock_outgoing_shipment_report"
        )
