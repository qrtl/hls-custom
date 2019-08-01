# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking Delivery Due Date',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': """
- Adds Delivery Due Date field to stock picking.
- Adjusts Scheduled Date proposal logic, considering lead time setting per
delivery address.
    """,
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
}
