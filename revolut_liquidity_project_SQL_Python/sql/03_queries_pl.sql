-- P&L attribution diary (simple)
SELECT 
    t.transaction_date,
    t.product_type,
    SUM(t.amount * CASE 
        WHEN t.product_type = 'deposit' THEN 0.002  -- ingreso por invertir depósitos
        WHEN t.product_type = 'withdrawal' THEN -0.001 -- coste de liquidez
        ELSE 0.0005 
    END) AS estimated_pnl
FROM transactions t
WHERE t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY t.transaction_date, t.product_type
ORDER BY t.transaction_date DESC;