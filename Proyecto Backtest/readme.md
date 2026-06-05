# Cryptocurrency Strategy Backtesting

This project uses historical market data obtained through the Binance API to perform a comprehensive backtest of a cryptocurrency trading strategy, including the evaluation of key performance and risk metrics such as the Sharpe Ratio, Maximum Drawdown, and overall profitability.

## Objective

Evaluate the performance, risk, and robustness of the trading strategy using historical cryptocurrency market data.

## Project Structure

The project consists of:

* A Python module (`.py`) containing reusable functions for data collection, indicator calculation, signal generation, and performance evaluation.
* A Jupyter Notebook used for analysis, visualization, and interpretation of backtesting results.
* An additional deployment script designed to run on a Raspberry Pi, allowing the strategy to automatically monitor markets and execute trade entry and exit signals in a live environment.

## Features

* Historical data retrieval from the Binance API.
* Technical indicator calculation and signal generation.
* Backtesting framework for strategy evaluation.
* Performance metrics including:

  * Sharpe Ratio
  * Maximum Drawdown
  * Annualized Return
  * Win Rate
  * Trade Duration Analysis
* Data visualization and performance reporting.

## Security Notice

For security reasons, all API keys and sensitive credentials have been removed from the project files.

## Technologies Used

* Python
* Pandas
* NumPy
* Binance API
* Jupyter Notebook
* Raspberry Pi
* Data Visualization Libraries

## Contact

**Email:** [hsalas2003@gmail.com](mailto:hsalas2003@gmail.com)
