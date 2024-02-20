# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Delivery Due Date",
    "version": "12.0.1.0.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Stock",
    "license": "AGPL-3",
    "depends": ["sale_stock", "sale_order_get_due_date"],
    "data": ["views/res_partner_views.xml", "views/stock_picking_views.xml"],
    "installable": True,
}
