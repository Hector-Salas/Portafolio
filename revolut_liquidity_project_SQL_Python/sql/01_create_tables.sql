-- Customer Transaction Table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT,
    product_type VARCHAR(20), -- 'deposit', 'withdrawal', 'investment_purchase', 'investment_redeem'
    amount DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'EUR',
    transaction_date DATE,
    value_date DATE
);

-- Short-term investment table
CREATE TABLE IF NOT EXISTS short_term_investments (
    investment_id SERIAL PRIMARY KEY,
    investment_name VARCHAR(50),
    as_of_date DATE,
    units_held DECIMAL(20,6),
    nav_per_unit DECIMAL(10,4),
    total_value DECIMAL(15,2)
);

-- Table of interest rates (curve)
CREATE TABLE IF NOT EXISTS interest_rates (
    rate_date DATE,
    tenor VARCHAR(10),
    rate_percent DECIMAL(6,4)
);

INSERT INTO transactions (customer_id, product_type, amount, currency, transaction_date, value_date)
SELECT 
    floor(random() * 10000 + 1)::int,
    (array['deposit', 'withdrawal', 'investment_purchase', 'investment_redeem'])[floor(random() * 4 + 1)],
    round((random() * 5000 + 10)::numeric, 2),
    'EUR',
    CURRENT_DATE - (random() * 45)::int + (random() * 45)::int,   
    CURRENT_DATE - (random() * 45)::int + (random() * 45)::int + (random() * 2)::int
FROM generate_series(1, 50000);

INSERT INTO short_term_investments (investment_name, as_of_date, units_held, nav_per_unit, total_value)
SELECT 
    'Revolut Money Fund',
    CURRENT_DATE - (random() * 90)::int,
    round((random() * 10000)::numeric, 2),
    round((random() * 100 + 1)::numeric, 4),
    round((random() * 1000000)::numeric, 2)
FROM generate_series(1, 90);

INSERT INTO interest_rates (rate_date, tenor, rate_percent)
SELECT 
    CURRENT_DATE - (random() * 90)::int,
    tenor,
    2.5 + random() * 2
FROM generate_series(1, 90), (VALUES ('ON'), ('1W'), ('1M'), ('3M')) AS t(tenor);