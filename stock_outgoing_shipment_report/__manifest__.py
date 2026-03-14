# Copyright 2020-2021 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Outgoing Shipment Report",
    "version": "18.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co",
    "author": "Quartile",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "delivery",
        "sale_order_line_client_order_ref",
        "sale_order_line_note",
        "stock_secondary_unit",
        "sale_order_dispatch_date",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_outgoing_shipment_report_data.xml",
        "views/delivery_carrier_views.xml",
        "views/res_partner_views.xml",
        "views/stock_outgoing_shipment_report_views.xml",
    ],
}
