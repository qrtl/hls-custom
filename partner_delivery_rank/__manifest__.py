# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Partner Delivery Rank",
    "summary": "Assign a rank to partners as delivery destinations and "
    "propagate it to sales orders and invoices for aggregation by rank.",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "website": "https://www.quartile.co",
    "author": "Quartile",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["account", "sale"],
    "data": [
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
}
