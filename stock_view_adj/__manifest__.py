# Copyright 2019 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock View Adj",
    "version": "18.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co",
    "author": "Quartile",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product_expiry"],
    "data": [
        "views/stock_quant_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
    ],
}
