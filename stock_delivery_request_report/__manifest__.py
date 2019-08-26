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
This module adds a py3o stock picking report.
    """,
    'depends': [
        'stock_picking_delivery_due_date',
        'report_py3o',
        'stock_picking_batch',
    ],
    'data': [
        #'report.xml',
        'view/stock_picking_batch.xml',
        'wizards/stock_picking_report_wizard_views.xml',
    ],
    'installable': True,
}
