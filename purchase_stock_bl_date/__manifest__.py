# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Stock Bl Date",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["purchase_stock", "product_cost_price_avco_sync"],
    "data": ["views/purchase_order_views.xml", "views/stock_picking_views.xml"],
}
