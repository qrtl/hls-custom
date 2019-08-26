# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Delivery Request Report',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': """
This module adds a py3o delivery request report based on stock picking batch.
    """,
    'depends': [
        'stock_picking_batch',
        'delivery',
        'report_py3o',
        'stock_picking_delivery_due_date',
    ],
    'data': [
        #'report.xml',
        'view/delivery_views.xml',
        'view/stock_picking_views.xml',
        'view/stock_picking_batch_views.xml',
        'wizards/stock_picking_report_wizard_views.xml',
    ],
    'installable': True,
}
