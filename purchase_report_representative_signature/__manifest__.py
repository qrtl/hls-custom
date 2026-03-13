# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Report Representative Signature",
    "summary": "Provide representative signing information for purchase reports.",
    "version": "18.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "category": "Reporting",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "report/purchase_order_templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
