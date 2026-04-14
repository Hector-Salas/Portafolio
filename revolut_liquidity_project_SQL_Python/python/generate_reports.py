# python/generate_reports.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from connect_db import get_db_connection

os.makedirs('outputs/charts', exist_ok=True)
os.makedirs('outputs/reports', exist_ok=True)

def run_query(sql_query):
    """Execute an SQL query and return a DataFrame"""
    conn = get_db_connection()
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

def plot_liquidity_gap():
    sql = """
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
        WHERE transaction_date >= CURRENT_DATE - INTERVAL '60 days'
        GROUP BY transaction_date
    )
    SELECT 
        bucket,
        SUM(net_flow) AS total_net_flow
    FROM bucket_flows
    GROUP BY bucket
    ORDER BY 
        CASE bucket
            WHEN 'T+1' THEN 1
            WHEN 'T+7' THEN 2
            WHEN 'T+30' THEN 3
            ELSE 4
        END;
    """
    df = run_query(sql)
    if df.empty:
        print("There is no data for the liquidity gap")
        return
    plt.figure(figsize=(8,4))
    sns.barplot(data=df, x='bucket', y='total_net_flow', hue='bucket', legend=False, palette='coolwarm')
    plt.title('Liquidity Gap by Bucket (Net Flow)')
    plt.ylabel('Net Flow (EUR)')
    plt.tight_layout()
    plt.savefig('outputs/charts/liquidity_gap.png')
    plt.close()
    print("+ Saved liquidity chart")

def plot_pnl_by_product():
    sql = """
    SELECT 
        t.transaction_date,
        t.product_type,
        SUM(t.amount * CASE 
            WHEN t.product_type = 'deposit' THEN 0.002
            WHEN t.product_type = 'withdrawal' THEN -0.001
            ELSE 0.0005 
        END) AS estimated_pnl
    FROM transactions t
    WHERE t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY t.transaction_date, t.product_type
    ORDER BY t.transaction_date;
    """
    df = run_query(sql)
    if df.empty:
        print("No P&L data available")
        return
    plt.figure(figsize=(10,5))
    for prod in df['product_type'].unique():
        subset = df[df['product_type'] == prod]
        plt.plot(subset['transaction_date'], subset['estimated_pnl'], label=prod)
    plt.title('Daily P&L Attribution by Product (last 30 days)')
    plt.xlabel('Date')
    plt.ylabel('P&L (EUR)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/charts/pnl_by_product.png")
    plt.close()
    print("+ Saved P&L Chart")

def plot_drawdown():
    sql = """
    WITH cumulative AS (
        SELECT 
            transaction_date,
            SUM(CASE WHEN product_type='deposit' THEN amount ELSE -amount END) OVER (ORDER BY transaction_date) AS running_balance
        FROM transactions
    )
    SELECT 
        transaction_date,
        running_balance,
        MAX(running_balance) OVER (ORDER BY transaction_date) AS peak,
        (running_balance - MAX(running_balance) OVER (ORDER BY transaction_date)) AS drawdown
    FROM cumulative;
    """
    df = run_query(sql)
    if df.empty:
        return
    plt.figure(figsize=(10,4))
    plt.fill_between(df['transaction_date'], df['drawdown'], 0, color='red', alpha=0.3, label='Drawdown')
    plt.plot(df['transaction_date'], df['running_balance'], label='Liquidity balance')
    plt.title('Liquidity Drawdown Analysis')
    plt.xlabel('Date')
    plt.ylabel('EUR')
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/charts/drawdown.png')
    plt.close()
    print("+ Saved drawdown chart")

def generate_insights():
    """Generate a text file with automatic insights"""
    sql_liquidity = """
    SELECT AVG(net_cash_flow) as avg_flow, MIN(net_cash_flow) as min_flow 
    FROM mv_cash_flows_by_bucket;
    """
    df_flow = run_query(sql_liquidity)
    
    sql_behaviour = """
    SELECT 
        EXTRACT(DOW FROM transaction_date) as dow,
        AVG(amount) as avg_withdrawal
    FROM transactions
    WHERE product_type='withdrawal'
    GROUP BY dow
    ORDER BY dow;
    """
    df_behave = run_query(sql_behaviour)
    
    insights = []
    if not df_flow.empty:
        avg_flow = df_flow['avg_flow'].iloc[0]
        min_flow = df_flow['min_flow'].iloc[0]
        if min_flow < 0:
            insights.append(f"⚠️ Liquidity stress: minimum daily net flow of {min_flow:,.0f} EUR.")
        if avg_flow < 0:
            insights.append("📉 Average net cash flow negative – structural outflow.")
    
    if not df_behave.empty:
        weekend_avg = df_behave[df_behave['dow'].isin([5,6])]['avg_withdrawal'].mean()
        weekday_avg = df_behave[~df_behave['dow'].isin([5,6])]['avg_withdrawal'].mean()
        if weekend_avg > weekday_avg * 1.2:
            insights.append("📅 Weekend withdrawal clustering observed – review liquidity for Saturdays/Sundays.")
    
    if not insights:
        insights.append(" Liquidity and P&L within normal ranges.")
    
    with open('outputs/insights_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"Revolut-style Analysis – {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*50 + "\n")
        for i, insight in enumerate(insights, 1):
            f.write(f"{i}. {insight}\n")
    print("- Insights saved at outputs/insights_summary.txt")

def generate_all_reports_and_charts():
    """Main function that runs all reports"""
    plot_liquidity_gap()
    plot_pnl_by_product()
    plot_drawdown()
    generate_insights()
    print(" - All generated reports and graphs.")