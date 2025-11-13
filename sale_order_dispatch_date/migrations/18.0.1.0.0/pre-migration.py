def migrate(cr, version):
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name='stock_picking' AND column_name='delivery_due_date'
        LIMIT 1
    """)
    if not cr.fetchone():
        return
    cr.execute("""
        UPDATE stock_picking
           SET date_deadline = delivery_due_date
         WHERE delivery_due_date IS NOT NULL
           AND state NOT IN ('done','cancel')
    """)
