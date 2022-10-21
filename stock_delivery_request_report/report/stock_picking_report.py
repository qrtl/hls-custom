# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class StockPickingReport(models.TransientModel):
    _name = "stock.picking.report"

    batch_id = fields.Many2one("stock.picking.batch")
    line_ids = fields.One2many(
        "stock.picking.report.line",
        inverse_name="report_id",
    )
    company_id = fields.Many2one("res.company")

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return _(
            "Delivery Request (%s - %s)"
            % (
                self.batch_id.carrier_id.name,
                fields.Date.to_string(self.batch_id.ship_date),
            )
        )

    def _create_delivery_request_form(self, bp):
        report = self.create(
            {"company_id": self.env.user.company_id.id, "batch_id": bp.id}
        )
        self.env["stock.picking.report.line"]._create_delivery_request_lines(
            report, bp.picking_ids
        )
        return report.id


class StockPickingReportLine(models.TransientModel):
    _name = "stock.picking.report.line"

    report_id = fields.Many2one(
        "stock.picking.report",
    )
    move_id = fields.Many2one(
        "stock.move",
    )
    report_qty = fields.Float(
        digits=dp.get_precision("Product Unit of Measure"),
    )
    report_uom = fields.Char()
    picking_id = fields.Many2one(
        related="move_id.picking_id",
    )
    partner_id = fields.Many2one(
        related="picking_id.partner_id",
    )

    def _create_delivery_request_lines(self, report, picking_ids):
        for picking in picking_ids:
            for move in picking.move_lines:
                # move record should not show in the report if there is no
                # available quantity
                quantity = move.quantity_done or move.reserved_availability
                if quantity > 0:
                    secondary_uom = move.product_id.stock_secondary_uom_id
                    if secondary_uom:
                        report_uom = secondary_uom.name
                        factor = secondary_uom.factor * move.product_uom.factor
                        report_qty = float_round(
                            quantity / (factor or 1.0),
                            precision_rounding=secondary_uom.uom_id.factor,
                        )
                    else:
                        report_uom = move.product_uom.name
                        report_qty = quantity
                    self.create(
                        {
                            "report_id": report.id,
                            "move_id": move.id,
                            "report_qty": report_qty,
                            "report_uom": report_uom,
                        }
                    )
