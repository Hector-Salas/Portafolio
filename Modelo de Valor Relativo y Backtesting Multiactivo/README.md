
# Relative Value Model

**Objective:** Demonstrate skills in financial modeling, data validation, and automated reporting, aligned with a Data Science Analyst role.

## Responsibilities Covered

* **Mathematical Models** – Equity Risk Premium (ERP) analysis for equities versus bonds, and the Gold/S&P 500 ratio.
* **Market Data Validation** – Outlier detection using the Median Absolute Deviation (MAD) method.
* **Regulatory & Operational Reporting** – Automated daily generation of `cierre_operaciones.csv` and analytical reports.

## Methodology Overview

* **ERP** = Earnings Yield (1/PE) – TNX Yield (U.S. 10-Year Treasury Bond).
* **Z-Score Analysis** using a rolling 360-day window (configurable).
* **Investment Signal Rules:**

  * Z > 1.5 → Overweight equities (60%)
  * Z < -1.5 → Underweight equities (40%)
  * Otherwise → Neutral allocation (50%)
* **Outlier Detection:** MAD method with a 5-day rolling window and a threshold of 3.0.
* **Commodities Analysis:** Gold/S&P 500 ratio using the same Z-score methodology.
* **Correlation Analysis:** Correlation matrix of returns for the S&P 500, U.S. Treasury bonds, and gold.

## How to Run

1. Install dependencies:

```bash
pip install pandas numpy yfinance scipy seaborn matplotlib
```

2. Run the notebook cell by cell, or execute all cells using **Run All**.
3. Reports are automatically generated in the `reports/` directory.

## Contact

**Email:** [hsalas2003@gmail.com](mailto:hsalas2003@gmail.com)
