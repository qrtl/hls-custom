# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Report Quantity Total",
    "summary": "Show total quantities grouped by unit in the purchase order report.",
    "version": "18.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "category": "Reporting",
    "license": "AGPL-3",
    "depends": ["purchase_order_secondary_unit"],
    "data": [
        "security/ir.model.access.csv",
        "report/purchase_order_templates.xml",
    ],
    "installable": True,
}
