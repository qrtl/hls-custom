# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tools.sql import column_exists


def pre_init_hook(env):
    for table in ("sale_order", "account_move"):
        if not column_exists(env.cr, table, "end_customer"):
            env.cr.execute(f"ALTER TABLE {table} ADD COLUMN end_customer VARCHAR")
