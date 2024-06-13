import pandas as pd

def update_warehouse_inventory(production_data, sales_data, initial_inventory, store_orders, resources):
    # Initialize the inventory DataFrame with the necessary columns
    inventory = pd.DataFrame(columns=['Period', 'Code', 'Received', 'Sold', 'Inventory', 'Activity', 'Resource', 'Capacity', 'Days Required'])

    # Initialize columns
    inventory['Period'] = production_data['period']
    inventory['Code'] = production_data['code']
    inventory['Received'] = production_data['Actual Production']
    inventory['Days Required'] = production_data['Production Days']
    inventory = inventory.merge(sales_data[['period', 'code', 'forecast']], left_on=['Period', 'Code'], right_on=['period', 'code'], how='left')
    inventory['Sold'] = inventory['forecast'].fillna(0).astype(int)  # Replace NaN with 0 for periods without sales data and cast to int
    inventory.drop(columns=['period', 'code', 'forecast'], inplace=True)

    # Ensure initial_inventory column names are consistent
    initial_inventory.columns = ['Code', 'initial_inventory']

    # Calculate initial inventory for each code
    inventory = inventory.merge(initial_inventory, on='Code', how='left')
    inventory['Inventory'] = inventory['initial_inventory'].astype(int)

    # Ensure store orders columns are consistent
    store_orders.columns = ['Store', 'Order', 'Day Delivery', 'Code', 'Quantity']

    # Merge with store orders to align shipments
    inventory = inventory.merge(store_orders, left_on=['Period', 'Code'], right_on=['Day Delivery', 'Code'], how='left')

    # Calculate inventory levels
    for code in inventory['Code'].unique():
        code_inventory = inventory[inventory['Code'] == code]
        inventory.loc[inventory['Code'] == code, 'Inventory'] = (code_inventory['initial_inventory'].iloc[0] + code_inventory['Received'].cumsum() - code_inventory['Sold'].cumsum()).astype(int)

    # Assign resources for activities and filter columns
    receiving = inventory[inventory['Received'] > 0].copy()
    receiving['Activity'] = 'Receiving'
    receiving['Resource'] = 'Lift Truck'
    receiving['Capacity'] = resources.loc[(resources['resource'] == 'Lift Truck') & (resources['activity'] == 'Receiving'), 'capacity_per_day'].values[0] if not resources[(resources['resource'] == 'Lift Truck') & (resources['activity'] == 'Receiving')].empty else 0
    receiving = receiving[['Period', 'Code', 'Received', 'Activity', 'Resource', 'Capacity', 'Days Required']]

    picking_packing = inventory[inventory['Sold'] > 0].copy()
    picking_packing['Activity'] = 'Picking/Packing'
    picking_packing['Resource'] = 'Human'
    picking_packing['Capacity'] = resources.loc[(resources['resource'] == 'Human') & (resources['activity'] == 'Picking'), 'capacity_per_day'].values[0] + resources.loc[(resources['resource'] == 'Human') & (resources['activity'] == 'Packing'), 'capacity_per_day'].values[0] if not resources[(resources['resource'] == 'Human') & (resources['activity'] == 'Picking')].empty and not resources[(resources['resource'] == 'Human') & (resources['activity'] == 'Packing')].empty else 0
    picking_packing = picking_packing[['Period', 'Code', 'Sold', 'Activity', 'Resource', 'Capacity', 'Days Required']]

    # Filter for shipping
    shipping = picking_packing.copy()
    shipping['Activity'] = 'Shipping'
    shipping['Resource'] = 'Human'
    shipping['Capacity'] = resources.loc[(resources['resource'] == 'Human') & (resources['activity'] == 'Shipping'), 'capacity_per_day'].values[0] if not resources[(resources['resource'] == 'Human') & (resources['activity'] == 'Shipping')].empty else 0
    shipping['Store'] = inventory['Store']
    shipping['Day Delivery'] = inventory['Day Delivery']
    shipping['Quantity'] = inventory['Quantity']

    # Ensure the correct columns are in shipping DataFrame and remove NaN rows
    shipping = shipping[['Period', 'Code', 'Store', 'Day Delivery', 'Quantity', 'Sold', 'Activity', 'Resource', 'Capacity', 'Days Required']]
    shipping.dropna(subset=['Store', 'Day Delivery', 'Quantity'], inplace=True)

    return receiving, picking_packing, shipping

def main():
    # Load production data from factory.py (simulated production plan)
    production_file = 'simulated_production_plan.csv'
    production_data = pd.read_csv(production_file)

    # Load sales data from demand_forecasts.csv
    sales_file = 'demand_forecasts.csv'
    sales_data = pd.read_csv(sales_file, delimiter=';')

    # Load initial inventory data
    initial_inventory_file = 'initial_inventory.csv'
    initial_inventory = pd.read_csv(initial_inventory_file, delimiter=';')

    # Load store orders data
    store_orders_file = 'store_orders.csv'
    store_orders = pd.read_csv(store_orders_file)

    # Load resources data
    resources_file = 'resources.csv'
    resources = pd.read_csv(resources_file, delimiter=';')

    # Update warehouse inventory and separate activities
    receiving, picking_packing, shipping = update_warehouse_inventory(production_data, sales_data, initial_inventory, store_orders, resources)

    # Output results
    print("Receiving Data:")
    print(receiving)
    print("Picking/Packing Data:")
    print(picking_packing)
    print("Shipping Data:")
    print(shipping)

    # Save updated data to CSVs
    receiving.to_csv('receiving.csv', index=False)
    picking_packing.to_csv('picking_packing.csv', index=False)
    shipping.to_csv('shipping.csv', index=False)

if __name__ == "__main__":
    main()
