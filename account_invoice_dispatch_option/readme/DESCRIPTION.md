This module adds the fields use_company_invoice and invoice_send_method
to both res.partner and account.invoice models and includes these fields
in the filters and group by options of account.invoice. The values from
res.partner are propagated to account.invoice, helping to determine
whether an invoice needs to be sent to customers or not.
