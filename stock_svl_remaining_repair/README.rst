==========================
Stock SVL Remaining Repair
==========================

This module is intended for one-time installation on the target database.

When the module is installed, it automatically:

* applies the known quantity pre-fix for internal reference ``86406``
* repairs stock valuation layer ``remaining_qty`` and ``remaining_value``
* creates adjustment SVLs and journal entries when required
* updates ``standard_price`` where needed
* creates backup tables for all changes

No menu or manual wizard is provided. The repair runs from ``post_init_hook``.
