from binance.client import Client
from binance.enums import *
import pandas as pd
import os
import time
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
import seaborn as sns
from scipy import stats
import ta

API_KEY = "secreta" 
API_SECRET = "confidencial"
client = Client(API_KEY,API_SECRET, tld = "com")

def load_binance_ohlcv(symbol: str, interval: str = Client.KLINE_INTERVAL_15MINUTE, start_str: str = '1 Jan, 2023', end_str: str = None) -> pd.DataFrame:
    """
    Descarga datos OHLCV de Binance para el símbolo y período deseado.

    Args:
        symbol (str): Ticker (ej. 'BTCUSDT', 'ETHUSDT').
        interval (str): Intervalo de tiempo. Por defecto 1 hora.
        start_str (str): Fecha de inicio (ej. '30 days ago UTC', '2023-01-01').
        end_str (str): Fecha de fin (ej. '2023-12-31'). Si es None, se usa el momento actual.

    Returns:
        pd.DataFrame: DataFrame con columnas datetime, open, high, low, close, volume.
    """
    print(f"Descargando datos de {symbol} desde {start_str} hasta {end_str or 'ahora'} con intervalo {interval}...")
    
    # Consulta los datos
    if end_str:
        klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    else:
        klines = client.get_historical_klines(symbol, interval, start_str)

    # Estructura en DataFrame
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])

    # Limpieza y conversión de tipos
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('datetime', inplace=True)

    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df
#def preparar_datos --- df =preparar_datos()
#def signal(df) --- signal_df = signal(df)
def run_tp_sl(data, apalancamiento=2, tp=0.015, sl=-0.010,cost=0.0004):

    trades = []
    in_position = False
    entry_price = 0
    entry_index = None
    direction = 0  # 1 = long, -1 = short

    for i in range(len(data)):
        row = data.iloc[i]
        price = row['close']
        signal = row['signal']

        # Abrir operación
        if not in_position and signal != 0:
            in_position = True
            entry_price = price
            entry_index = data.index[i]
            direction = signal
            continue

        # Cierre por SL / TP / cambio de señal opuesta
        if in_position:
            pct_change = (price - entry_price) / entry_price * direction
            close_trade = False

            # Cerrar por TP/SL
            if pct_change >= tp or pct_change <= sl:
                close_trade = True

            # O cerrar si la señal cambia en dirección opuesta
            elif signal == -direction and signal != 0:
                close_trade = True

            if close_trade:
                exit_index = data.index[i]
                net_return = (pct_change - cost) * apalancamiento

                trades.append({
                    'entry_time': entry_index,
                    'exit_time': exit_index,
                    'entry_price': entry_price,
                    'exit_price': price,
                    'direction': direction,
                    'pct_change': pct_change,
                    'net_return': net_return
                })

                # Reset posición
                in_position = False
                entry_price = 0
                entry_index = None
                direction = 0

    return pd.DataFrame(trades)
#returns_df = run_tp_sl(signal_df)
def calcular_rendimiento_acumulado(trades_df):
    trades_df['cumulative_return'] = (1 + trades_df['net_return']).cumprod() - 1
    return trades_df
def evaluar_metricas(trades_df, risk_free_rate=0.08):
    returns = trades_df['net_return']
    
    # Win rate
    wins = (returns > 0).sum()
    win_rate = wins / len(returns) if len(returns) > 0 else 0

    # Sharpe Ratio (anualizado aproximado si 96 trades/día por marco 15min)
    mean_ret = returns.mean()
    std_ret = returns.std()
    sharpe_ratio = ((mean_ret - risk_free_rate) / std_ret) * np.sqrt(364) if std_ret > 0 else 0

    # Max drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    return {
        'win_rate': round(win_rate, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'max_drawdown': round(max_drawdown, 2),
        'total_trades': len(returns),
        'total_return': round(cumulative.iloc[-1] - 1, 2) if not cumulative.empty else 0
    }
#df_m = calcular_rendimiento_acumulado(returns_df)
#metricas = evaluar_metricas(returns_df)
#print(metricas)
def heatmap_monthly_returns(trades_df, date_col='entry_time', return_col='net_return'):
    """
    Genera un mapa de calor de retornos mensuales usando la columna de fecha proporcionada.

    Parámetros:
        trades_df (pd.DataFrame): DataFrame con columnas de fecha y retornos.
        date_col (str): Columna con fechas (ej. 'entry_time').
        return_col (str): Columna con retornos (ej. 'net_return').

    Salida:
        Mapa de calor (heatmap) con retornos mensuales.
    """

    # Asegurarse de que la columna de fecha sea datetime
    trades_df[date_col] = pd.to_datetime(trades_df[date_col])

    # Extraer año y mes
    trades_df['year'] = trades_df[date_col].dt.year
    trades_df['month'] = trades_df[date_col].dt.month

    # Agrupar retornos por año y mes
    monthly_returns = trades_df.groupby(['year', 'month'])[return_col].sum().unstack(fill_value=0)

    # Reemplazar números de mes por nombres
    monthly_returns.columns = [pd.to_datetime(f'2023-{m}-01').strftime('%b') for m in monthly_returns.columns]

    # Ordenar meses
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_returns = monthly_returns.reindex(columns=months_order, fill_value=0)

    # Graficar mapa de calor
    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly_returns, annot=True, fmt=".2%", cmap='RdYlGn', center=0, linewidths=0.5)
    plt.title("Mapa de Calor de Retornos Mensuales")
    plt.ylabel("Año")
    plt.xlabel("Mes")
    plt.tight_layout()
    plt.show()
#heatmap_monthly_returns(returns_df)
def plot_annual_returns(trades_df, date_col='entry_time', return_col='net_return'):
    """
    Gráfico de barras con retornos anuales y valores numéricos en cada barra.
    """
    # Calcular retornos anuales
    trades_df[date_col] = pd.to_datetime(trades_df[date_col])
    annual_returns = trades_df.groupby(trades_df[date_col].dt.year)[return_col].sum()
    # Crear gráfico
    plt.figure(figsize=(10, 4))
    bars = plt.bar(annual_returns.index, annual_returns, 
                   color=np.where(annual_returns >= 0, 'green', 'red'))
    # Añadir etiquetas con los valores
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2%}',  # Formato porcentual con 2 decimales
                 ha='center', va='bottom', fontsize=10)
    plt.title("Retornos Anuales Acumulados (con valores)")
    plt.xlabel("Año")
    plt.ylabel("Retorno (%)")
    plt.xticks(annual_returns.index)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
# plot_annual_returns(returns_df)
def monte_carlo_simulation(trades_df, return_col="net_return", method="compound", n_sim=200):
    """
    Simulación Monte Carlo de retornos acumulados (simple o compuesta).

    Parámetros:
        trades_df (pd.DataFrame): DataFrame con columna de retornos históricos.
        return_col (str): Nombre de la columna de rendimientos (%), ej. 'net_return'.
        method (str): 'simple' para suma acumulada, 'compound' para capitalización compuesta.
        n_sim (int): Número de simulaciones.

    Salida:
        Gráfico con percentiles 1%, 50% y 99% y el retorno real.
    """
    returns = trades_df[return_col].fillna(0).values
    n = len(returns)
    simulations = []

    for _ in tqdm(range(n_sim), desc="Simulando"):
        shuffled = np.random.permutation(returns)
        if method == "simple":
            sim = np.cumsum(shuffled) * 100  # % acumulado
        else:
            sim = (np.cumprod(1 + shuffled) - 1) * 100  # interés compuesto
        simulations.append(sim)

    df_sim = pd.DataFrame(simulations).T
    p_99 = np.percentile(df_sim, 99, axis=1)
    p_50 = np.percentile(df_sim, 50, axis=1)
    p_01 = np.percentile(df_sim, 1, axis=1)

    # Curva real
    if method == "simple":
        real_curve = np.cumsum(returns) * 100
    else:
        real_curve = (np.cumprod(1 + returns) - 1) * 100

    # Gráfico
    plt.figure(figsize=(18, 7))
    plt.plot(p_99, label="Percentil 99", color="#39B3C7")
    plt.plot(p_50, label="Median", color="#39B3C7")
    plt.plot(p_01, label="Percentil 1", color="#39B3C7")
    plt.plot(real_curve, label="Retorno real", color="blue", linewidth=3, alpha=0.7)
    plt.fill_between(range(n), p_01, p_99, color="#669FEE", alpha=0.2, label="Área Monte Carlo")

    plt.title("Simulación Monte Carlo con Retornos Históricos", size=18)
    plt.ylabel("Retorno acumulado (%)", size=13)
    plt.xlabel("Número de operaciones")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
#monte_carlo_simulation(returns_df, return_col="net_return", method="compound", n_sim=200)
def simulate_compounded_growth(returns_df, initial_capital=10000):
    capital = initial_capital
    capital_history = []
    for idx, row in returns_df.iterrows():
        capital *= (1 + row['net_return'])
        capital_history.append({
            'exit_time': row['exit_time'],
            'capital': capital
        })
    return pd.DataFrame(capital_history)
"""
capital_simulation = simulate_compounded_growth(returns_df)
plt.figure(figsize=(10, 5))
plt.plot(capital_simulation['exit_time'], capital_simulation['capital'], 
         marker='', linestyle='-', color='blue', label='Capital acumulado')
final_capital = capital_simulation['capital'].iloc[-1]
plt.text(
    capital_simulation['exit_time'].iloc[-1], 
    final_capital, 
    f'Capital final: ${final_capital:,.2f}', 
    ha='right', va='bottom', 
    fontsize=12, 
    bbox=dict(facecolor='white', alpha=0.8)
)
plt.title("Crecimiento de Capital (Interés Compuesto)")
plt.xlabel("Fecha")
plt.ylabel("Capital ($)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
"""