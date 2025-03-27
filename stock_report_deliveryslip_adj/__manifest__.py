# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Report Delivery Slip Adjustments",
    "version": "12.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "depends": [
        "sale_stock",
        "sale_order_delivery_date",
        "sale_order_line_customer_reference",
        "stock_picking_report_valued",
        "stock_move_line_secondary_done",
    ],
    "data": [
        "data/report_deliveryslip_data.xml",
        "report/report_deliveryslip.xml",
    ],
    "installable": True,
}
