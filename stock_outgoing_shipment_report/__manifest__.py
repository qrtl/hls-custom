# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Outgoing Shipment Report",
    "summary": "",
    "version": "12.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale_order_line_customer_reference", "stock_picking_delivery_due_date", "stock_secondary_unit"],
    "data": [
        "data/stock_outgoing_shipment_report_data.xml",
        "views/delivery_carrier_views.xml",
        "views/res_partner_views.xml",
        "views/stock_outgoing_shipment_report_views.xml",
    ],
}