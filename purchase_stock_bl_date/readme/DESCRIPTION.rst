This module adds B/L Date fields to the purchase order and the picking.  B/L Date assigned
in the purchase receipt is used for capturing the currency rate for the unit price
calculation, which is the basis of inventory valuation.

Note that this module only adjusts the logic where currency rate is captured.
Adjusting the date of stock moves or journal entries is outside the scope of this module.

Background:
~~~~~~~~~~~

Depending on the incoterms of the purchase transaction in international trades, the
ownership transfer of the purchased products takes place before they arrive at the
domestic warehouse (i.e. when products are loaded in cargo in the origin country), while
the receipt operation in Odoo, for practical reasons, have to be done when the products
are received at the warehouse.  This results in an inaccurate valuation of the inventory,
which should be avoided.
