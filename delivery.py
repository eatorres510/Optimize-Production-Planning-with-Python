import pandas as pd

def allocate_deliveries(shipping_data, trucks):
    # Initialize columns
    shipping_data['Delivery Truck'] = ''
    shipping_data['Delivery Capacity'] = 0
    shipping_data['Deliveries Made'] = 0

    # Define truck capacities and maximum deliveries per day
    truck_capacities = trucks.set_index('Truck')['Capacity'].to_dict()
    max_deliveries_per_day = trucks.set_index('Truck')['Max Deliveries'].to_dict()

    # Iterate over each period and allocate deliveries
    for index, row in shipping_data.iterrows():
        required_capacity = row['Quantity']
        deliveries_needed = 0

        for truck, capacity in truck_capacities.items():
            if required_capacity <= 0:
                break
            possible_deliveries = min(max_deliveries_per_day[truck], -(-required_capacity // capacity))
            deliveries_needed += possible_deliveries
            shipping_data.at[index, 'Delivery Truck'] += f"{truck} x {possible_deliveries}, "
            shipping_data.at[index, 'Delivery Capacity'] += capacity * possible_deliveries
            required_capacity -= capacity * possible_deliveries

        # Calculate usage percentage based on delivery capacity
        shipping_data.at[index, 'Deliveries Made'] = deliveries_needed
        shipping_data.at[index, 'Capacity Used (%)'] = (row['Quantity'] / shipping_data.at[index, 'Delivery Capacity']) * 100 if shipping_data.at[index, 'Delivery Capacity'] > 0 else 0

        # Remove trailing comma and space
        shipping_data.at[index, 'Delivery Truck'] = shipping_data.at[index, 'Delivery Truck'].strip(', ')

    return shipping_data

def main():
    # Load shipping data from warehouse.py
    shipping_file = 'shipping.csv'
    shipping_data = pd.read_csv(shipping_file)

    # Load truck data
    trucks_file = 'trucks.csv'
    trucks = pd.read_csv(trucks_file)

    # Allocate deliveries
    allocated_shipping = allocate_deliveries(shipping_data, trucks)

    # Output results
    print("Delivery Information:")
    print(allocated_shipping[['Period', 'Store', 'Day Delivery', 'Delivery Truck', 'Deliveries Made', 'Capacity Used (%)']])

    # Save updated data to CSV
    allocated_shipping.to_csv('allocated_shipping.csv', index=False)

if __name__ == "__main__":
    main()
