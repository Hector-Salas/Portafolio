# Mint Classics Warehouse Optimization Analysis

## Project Overview

Mint Classics, a retailer of classic model cars and vehicles, is considering closing one of its storage facilities to reduce operational costs. The objective of this project is to analyze inventory, sales performance, and warehouse utilization data to identify the warehouse that could be closed with minimal impact on customer service and business operations.

---

## Business Problem

The company wants to reduce storage costs by closing one warehouse while maintaining timely service to customers. The analysis focuses on inventory distribution, sales activity, product demand, and warehouse capacity utilization to support a data-driven decision.

---

## Tools & Technologies

* MySQL
* SQL
* Python
* Pandas
* Jupyter Notebook
* Tableau Public

---

## Data Quality Assessment

Before performing the analysis, the database was reviewed to ensure data quality and integrity.

Checks performed:

* Missing values in critical fields
* Duplicate records
* Invalid inventory quantities
* Invalid product prices
* Referential integrity between tables
* Warehouse assignment validation

The database showed no significant data quality issues that would affect the analysis.

---

## Analysis Performed

### Inventory Analysis

* Total inventory by warehouse
* Inventory value by warehouse
* Inventory distribution across storage facilities

### Sales Analysis

* Units sold by warehouse
* Product demand evaluation
* Identification of low-demand products

### Warehouse Utilization Analysis

* Capacity utilization comparison across warehouses
* Evaluation of available space in remaining facilities

### Product Performance Analysis

* Identification of slow-moving products
* Identification of products with no sales history

---

## Key Findings

### Warehouse D (South)

* Lowest inventory volume among all warehouses
* Lowest sales contribution
* Lowest inventory value
* Capacity utilization of 75%

### Warehouse B (East)

* Highest inventory value
* Contains several low-demand products
* Includes at least one product with no recorded sales

### Available Capacity

The remaining warehouses have sufficient unused capacity:

| Warehouse | Capacity Utilization |
| --------- | -------------------- |
| South (D) | 75%                  |
| North (A) | 72%                  |
| East (B)  | 67%                  |
| West (C)  | 50%                  |

These results suggest that the inventory currently stored in Warehouse D can be redistributed without significantly affecting customer service levels.

---

## Recommendation

After analyzing inventory levels, sales activity, inventory value, product demand, and warehouse utilization, Warehouse D appears to be the strongest candidate for closure. It has the lowest inventory volume, the lowest sales contribution, and the lowest inventory value among all warehouses. These findings suggest that closing Warehouse D would likely have the smallest impact on customer service and overall business operations.

Furthermore, the remaining warehouses have sufficient unused capacity to absorb Warehouse D's inventory without significantly affecting service levels. This indicates that inventory redistribution can be achieved while maintaining operational efficiency and timely customer deliveries.

Additionally, the analysis of product demand revealed several slow-moving products in Warehouse B, including at least one product with no recorded sales. While Warehouse B is not a strong candidate for closure due to its high inventory value, these findings highlight an opportunity to optimize inventory management and improve stock turnover.

Therefore, the recommended strategy is to close Warehouse D and redistribute its inventory across the remaining warehouses while implementing inventory optimization initiatives, particularly in Warehouse B.

---

## Dashboard

Interactive Tableau Dashboard:

[(https://public.tableau.com/app/profile/hector.salas/viz/MintClassicsInventoryWarehousesOptimizationAnalysis/MintClassicsInventoryOptimizationAnalysis)]

---

## Skills Demonstrated

* SQL Querying
* Relational Database Analysis
* Data Cleaning & Validation
* Business Intelligence
* Inventory Analysis
* Data Visualization
* Business Recommendation Development
* Tableau Dashboard Design
