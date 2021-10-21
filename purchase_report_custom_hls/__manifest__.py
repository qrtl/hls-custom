# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Report Custom",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["purchase_stock", "report_common_hls", "purchase_order_secondary_unit"],
    "data": [
        "security/purchase_security.xml",
        "report/purchase_order_report_templates.xml",
        "views/purchase_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
