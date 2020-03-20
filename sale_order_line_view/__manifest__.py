# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Line View",
    "summary": "",
    "version": "12.0.1.0.2",
    "category": "Sales",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale",
        "sale_order_secondary_unit",
        "sale_order_secondary_unit_price",
    ],
    "data": ["views/sale_order_line_views.xml"],
}
