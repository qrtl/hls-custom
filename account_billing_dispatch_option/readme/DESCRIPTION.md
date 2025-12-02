This module adds the fields use_company_invoice and invoice_send_method
to both res.partner and account.billing models and includes these fields
in the filters and group by options of account.billing. The values from
res.partner are propagated to account.billing, helping to determine
whether a billing needs to be sent to customers or not.
