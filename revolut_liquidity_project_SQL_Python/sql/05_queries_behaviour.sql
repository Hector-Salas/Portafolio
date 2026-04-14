-- Deposit retention (behavioral analysis)
WITH daily_deposits AS (
    SELECT transaction_date, SUM(amount) AS deposits
    FROM transactions
    WHERE product_type = 'deposit'
    GROUP BY transaction_date
),
daily_withdrawals AS (
    SELECT transaction_date, SUM(amount) AS withdrawals
    FROM transactions
    WHERE product_type = 'withdrawal'
    GROUP BY transaction_date
)
SELECT 
    COALESCE(d.transaction_date, w.transaction_date) AS date,
    COALESCE(d.deposits, 0) AS deposits,
    COALESCE(w.withdrawals, 0) AS withdrawals,
    SUM(COALESCE(d.deposits, 0) - COALESCE(w.withdrawals, 0)) OVER (ORDER BY COALESCE(d.transaction_date, w.transaction_date)) AS net_position
FROM daily_deposits d
FULL OUTER JOIN daily_withdrawals w ON d.transaction_date = w.transaction_date
ORDER BY date DESC
LIMIT 30;