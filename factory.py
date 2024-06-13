import pandas as pd

def simulate_factory(production_plan, machines, actual_production_factor=1.0, delay_factor=0):
    production_plan['Actual Production'] = production_plan['forecast'] * actual_production_factor
    production_plan['Actual Delivery Date'] = production_plan['period'] + delay_factor
    production_plan = production_plan.merge(machines[['machine', 'code', 'capacity_per_day']], on='code')
    production_plan['Production Days'] = (production_plan['Actual Production'] / production_plan['capacity_per_day']).apply(lambda x: int(x) + (x % 1 > 0))
    return production_plan

def main():
    # Load production plan from CSV
    file_path = 'demand_forecasts.csv'
    production_plan = pd.read_csv(file_path, delimiter=';')

    # Load machine data from CSV
    machines_file = 'machines.csv'
    machines = pd.read_csv(machines_file, delimiter=';')

    # Simulate factory behavior
    actual_production_factor = 0.95  # 95% of planned production
    delay_factor = 2  # Delay by 2 periods
    simulated_plan = simulate_factory(production_plan, machines, actual_production_factor, delay_factor)

    # Output results
    print(simulated_plan)

    # Save simulated production plan to CSV
    simulated_plan.to_csv('simulated_production_plan.csv', index=False)

if __name__ == "__main__":
    main()
