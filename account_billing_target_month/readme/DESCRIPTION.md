This module extends `l10n_jp_summary_invoice` to add a **Target Month**
field to the billing document, computed automatically from the threshold
date. If the threshold date falls on the last day of the month, the target
month is set to the following month; otherwise it is set to the same month
as the threshold date.

The target month is also displayed as a prefix in the summary invoice PDF
title (e.g. "3 Summary Invoice").
