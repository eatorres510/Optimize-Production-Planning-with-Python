
## Production Planning and Delivery Optimization
This project includes three main modules: factory, warehouse, and delivery, designed to optimize production planning, warehouse management, and delivery scheduling.
## Overview
#Factory Module
Description: Simulates production planning using the Wagner-Whitin algorithm to balance setup and inventory costs.
Main Script: factory.py
Inputs: demand_forecasts.csv, machines.csv
Outputs: production_plan.csv

#Warehouse Module
Description: Manages receiving, picking/packing, and shipping activities within the warehouse.
Main Script: warehouse.py
Inputs: production_plan.csv, initial_inventory.csv, store_orders.csv
Outputs: warehouse_inventory.csv, shipping.csv

#Delivery Module
Description: Optimizes delivery scheduling based on truck capacities and delivery requirements.
Main Script: delivery.py
Inputs: shipping.csv, trucks.csv
Outputs: allocated_shipping.csv
## Usage
1. Factory Module
Place demand_forecasts.csv and machines.csv in the project directory.
Run the factory script:
python factory.py

2. Warehouse Module
Ensure production_plan.csv, initial_inventory.csv, and store_orders.csv are in the project directory.
Run the warehouse script:
python warehouse.py

3. Delivery Module
Ensure shipping.csv and trucks.csv are in the project directory.
Run the delivery script:
python delivery.py
## File Descriptions
Input Files
demand_forecasts.csv: Contains forecasted demand for each period.
machines.csv: Contains details about machines, their capacities, and production capabilities.
initial_inventory.csv: Contains initial inventory levels for each product code.
store_orders.csv: Contains orders from different stores with delivery days and quantities.
trucks.csv: Contains truck details, including capacities and maximum deliveries per day.

Output Files
production_plan.csv: Generated by factory.py, includes production schedules.
warehouse_inventory.csv: Generated by warehouse.py, includes updated warehouse inventory data.
shipping.csv: Generated by warehouse.py, includes shipping schedules.
allocated_shipping.csv: Generated by delivery.py, includes optimized delivery schedules.