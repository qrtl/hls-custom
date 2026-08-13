# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Partner Final Customer",
    "summary": "Add a final customer field to partners, searchable on sale orders",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "website": "https://www.quartile.co",
    "author": "Quartile",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale"],
    "data": [
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
}
