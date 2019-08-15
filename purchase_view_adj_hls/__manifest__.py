# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase View Adj HLS",
    "summary": "",
    "description": """
    """,
    'version': '12.0.1.0.0',
    "category": "Purchase",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_stock"
    ],
    "data": [
        'views/purchase_order_views.xml',
    ],
}