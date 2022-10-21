# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_repr


class InvoiceDeliveryReport(models.TransientModel):
    _name = "invoice.delivery.report"

    invoice_id = fields.Many2one("account.invoice")
    line_ids = fields.One2many("invoice.delivery.report.line", inverse_name="report_id")

    def _create_invoice_delivery_report(self, invoice):
        report = self.create({"invoice_id": invoice.id})
        self.env["invoice.delivery.report.line"]._create_invoice_delivery_report_lines(
            report, invoice.invoice_line_ids, invoice.date_from, invoice.date_to
        )
        return report.id

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return self.invoice_id._get_report_base_filename()


class InvoiceDeliveryReportLine(models.TransientModel):
    _name = "invoice.delivery.report.line"

    report_id = fields.Many2one("invoice.delivery.report")
    move_id = fields.Many2one("stock.move")
    sale_line_id = fields.Many2one("sale.order.line")
    invoice_line_id = fields.Many2one("account.invoice.line")
    currency_id = fields.Many2one(
        "res.currency", related="invoice_line_id.currency_id", readonly=True
    )
    secondary_uom_id = fields.Many2one("product.secondary.unit")
    product_uom = fields.Many2one("uom.uom")
    quantity = fields.Float(digits=dp.get_precision("Product Unit of Measure"))
    secondary_qty = fields.Float(
        compute="_compute_secondary_qty",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    qty_desc = fields.Text(compute="_compute_qty_desc")
    price_unit_desc = fields.Char(compute="_compute_price_unit_desc")
    price_subtotal = fields.Monetary(compute="_compute_amounts")
    price_total = fields.Monetary(compute="_compute_amounts")
    price_tax = fields.Monetary(compute="_compute_price_tax")
    tax_desc = fields.Char(compute="_compute_tax_desc")
    date_delivered = fields.Date()

    def _create_invoice_delivery_report_lines(
        self, report, invoice_line_ids, date_from, date_to
    ):
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        conflict_list = ""
        for il in invoice_line_ids.filtered(
            lambda x: x.product_id.type in ["product", "consu"] and x.sale_line_ids
        ).sorted(key=lambda x: x.sale_order_name or ""):
            sum_move_qty = 0.0
            for sl in il.sale_line_ids:
                moves = (
                    self.env["stock.move"]
                    .search(
                        [
                            ("sale_line_id", "=", sl.id),
                            ("state", "=", "done"),
                            ("date_delivered", ">=", date_from),
                            ("date_delivered", "<=", date_to),
                        ]
                    )
                    .sorted(key=lambda m: m.date_delivered)
                )
                for move in moves:
                    move_qty = (
                        move.quantity_done * -1
                        if move.picking_code == "incoming"
                        else move.quantity_done
                    )
                    self.create(
                        {
                            "report_id": report.id,
                            "invoice_line_id": il.id,
                            "move_id": move.id,
                            "sale_line_id": sl.id,
                            "secondary_uom_id": il.secondary_uom_id.id
                            if il.secondary_uom_id
                            else False,
                            "quantity": move_qty,
                            "product_uom": il.uom_id.id,
                            "date_delivered": move.date_delivered,
                        }
                    )
                    sum_move_qty += move_qty
            if (
                float_compare(sum_move_qty, il.quantity, precision_digits=precision)
                != 0
            ):
                conflict_list += _(
                    "\n%s (%s)\n- Delivered Quantity: %s\n- "
                    "Quantity in Invoice: %s\n"
                ) % (
                    il.product_id.display_name,
                    il.sale_line_ids[0].order_id.name,
                    sum_move_qty,
                    il.quantity,
                )
        if conflict_list:
            raise UserError(
                _(
                    "The quantity in the invoice and delivered "
                    "quantity are inconsistent for the following product(s):\n%s"
                )
                % (conflict_list)
            )
        for il in invoice_line_ids.filtered(
            lambda x: x.product_id.type not in ["product", "consu"]
            or not x.sale_line_ids
        ).sorted(key=lambda x: x.sale_order_name or ""):
            self.create(
                {
                    "report_id": report.id,
                    "invoice_line_id": il.id,
                    "move_id": False,
                    "sale_line_id": False,
                    "secondary_uom_id": il.secondary_uom_id.id
                    if il.secondary_uom_id
                    else False,
                    "quantity": il.quantity,
                    "product_uom": il.uom_id.id,
                }
            )

    @api.multi
    def _compute_secondary_qty(self):
        for rl in self.filtered(lambda x: x.secondary_uom_id):
            rl.secondary_qty = self._get_secondary_qty(
                rl.quantity, rl.product_uom, rl.secondary_uom_id
            )

    def _get_secondary_qty(self, quantity, product_uom, secondary_uom):
        factor = secondary_uom.factor * product_uom.factor
        qty = float_repr(quantity / (factor or 1.0), secondary_uom.uom_id.uom_dp)
        return qty

    @api.multi
    def _compute_qty_desc(self):
        for rl in self:
            ail = rl.invoice_line_id
            qty_desc = ""
            if ail.secondary_uom_price:
                sale_secondary_qty = rl._get_secondary_qty(
                    rl.quantity, rl.product_uom, rl.secondary_uom_id
                )
                qty_desc = (
                    str(sale_secondary_qty) + " " + rl.secondary_uom_id.name
                    if rl.secondary_uom_id
                    else str(sale_secondary_qty)
                )
            else:
                qty_desc = (
                    str(rl.quantity) + " " + rl.product_uom.name
                    if rl.product_uom
                    else str(rl.quantity)
                )
            if ail.product_id and ail.product_id.stock_secondary_uom_id:
                stock_secondary_uom = ail.product_id.stock_secondary_uom_id
                stock_secondary_qty = rl._get_secondary_qty(
                    rl.quantity, rl.product_uom, stock_secondary_uom
                )
                qty_desc += (
                    "\n("
                    + str(stock_secondary_qty)
                    + " "
                    + stock_secondary_uom.name
                    + ")"
                )
            rl.qty_desc = qty_desc

    @api.multi
    def _compute_price_unit_desc(self):
        for rl in self:
            ail = rl.invoice_line_id
            if ail.secondary_uom_price:
                rl.price_unit_desc = (
                    str(ail.secondary_uom_price) + " / " + rl.secondary_uom_id.name
                )
            else:
                rl.price_unit_desc = str(ail.price_unit)
                if ail.uom_id:
                    rl.price_unit_desc += " / " + ail.uom_id.name

    @api.multi
    def _compute_amounts(self):
        """the logic here should be consistent with _compute_price() method
        of account.invoice.line
        """
        for rl in self:
            ail = rl.invoice_line_id
            currency = ail.invoice_id and ail.invoice_id.currency_id or None
            price = ail.price_unit * (1 - (ail.discount or 0.0) / 100.0)
            taxes = False
            if ail.invoice_line_tax_ids:
                taxes = ail.invoice_line_tax_ids.compute_all(
                    price,
                    currency,
                    rl.quantity,
                    product=ail.product_id,
                    partner=ail.invoice_id.partner_id,
                )
            rl.price_subtotal = (
                taxes["total_excluded"] if taxes else rl.quantity * price
            )
            rl.price_total = taxes["total_included"] if taxes else rl.price_subtotal

    def _compute_price_tax(self):
        for rl in self:
            rl.price_tax = rl.price_total - rl.price_subtotal

    @api.multi
    def _compute_tax_desc(self):
        for rl in self:
            ail = rl.invoice_line_id
            tax_desc = ""
            for tax in ail.invoice_line_tax_ids:
                tax_desc += tax.description if not tax_desc else ", " + tax.description
            rl.tax_desc = tax_desc
