-- Materialized view of daily net flows (simulates ETL)
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_cash_flows_by_bucket AS
WITH daily_net_flow AS (
    SELECT 
        transaction_date,
        SUM(CASE WHEN product_type IN ('deposit', 'investment_redeem') THEN amount ELSE 0 END) AS inflows,
        SUM(CASE WHEN product_type IN ('withdrawal', 'investment_purchase') THEN amount ELSE 0 END) AS outflows
    FROM transactions
    GROUP BY transaction_date
)
SELECT 
    transaction_date,
    inflows,
    outflows,
    inflows - outflows AS net_cash_flow,
    SUM(inflows - outflows) OVER (ORDER BY transaction_date) AS cumulative_liquidity
FROM daily_net_flow;

-- Index for improving performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);