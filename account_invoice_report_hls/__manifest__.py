# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Report',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'license': 'AGPL-3',
    'description': """
Adds an invoice report in desired layout.
    """,
    'author': 'Quartile Limited',
    'depends': [
        'sale',
        'stock',
        'date_range',
        'report_common_hls',
        'report_py3o',
        'account_partner_company_bank',
        'account_invoice_secondary_unit',
    ],
    'data': [
        'views/res_company_views.xml',
        'views/account_invoice_views.xml',
        'views/stock_picking_views.xml',
        'wizard/invoice_delivery_report_wizard_views.xml',
        'report/invoice_delivery_report.xml',
    ],
    'installable': True,
}
