-- Liquidity Gap 
WITH bucket_flows AS (
    SELECT 
        transaction_date,
        SUM(CASE WHEN product_type = 'deposit' THEN amount ELSE -amount END) AS net_flow,
        CASE 
            WHEN transaction_date <= CURRENT_DATE + INTERVAL '1 day' THEN 'T+1'
            WHEN transaction_date <= CURRENT_DATE + INTERVAL '7 days' THEN 'T+7'
            WHEN transaction_date <= CURRENT_DATE + INTERVAL '30 days' THEN 'T+30'
            ELSE 'T+30+'
        END AS bucket
    FROM transactions
    WHERE transaction_date >= CURRENT_DATE
    GROUP BY transaction_date
)
SELECT 
    bucket,
    SUM(net_flow) AS total_net_flow,
    SUM(SUM(net_flow)) OVER (ORDER BY 
        CASE bucket
            WHEN 'T+1' THEN 1
            WHEN 'T+7' THEN 2
            WHEN 'T+30' THEN 3
            ELSE 4
        END) AS cumulative_gap
FROM bucket_flows
GROUP BY bucket;