import pandas as pd

def simulate_factory(production_plan, machines, actual_production_factor=1.0, delay_factor=0):
    production_plan['Actual Production'] = production_plan['forecast'] * actual_production_factor
    production_plan['Actual Delivery Date'] = production_plan['period'] + delay_factor
    production_plan = production_plan.merge(machines[['machine', 'code', 'capacity_per_day']], on='code')
    production_plan['Production Days'] = (production_plan['Actual Production'] / production_plan['capacity_per_day']).apply(lambda x: int(x) + (x % 1 > 0))
    return production_plan

def production_capacity_analysis(production_plan):
    total_capacity = production_plan.groupby('machine')['capacity_per_day'].sum()
    return total_capacity

def performance_analysis(production_plan):
    performance = production_plan.groupby('machine').agg({'Actual Production': 'sum', 'Production Days': 'sum'})
    performance['Performance'] = performance['Actual Production'] / performance['Production Days']
    return performance

def quality_control(production_plan):
    production_plan['Quality Check'] = production_plan['Actual Production'] * 0.98  # assuming 98% pass rate
    return production_plan

def maintenance_schedule(machines):
    machines['Next Maintenance'] = machines['usage_hours'] // 1000  # schedule maintenance every 1000 hours
    return machines

def human_machine_interface(production_plan):
    production_plan['HMI Status'] = 'Operational'  # Example HMI status
    return production_plan

def mom_intelligence(production_plan):
    production_summary = production_plan.groupby('period').agg({'Actual Production': 'sum', 'Production Days': 'sum'})
    production_summary['Efficiency'] = production_summary['Actual Production'] / production_summary['Production Days']
    return production_summary

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

    # Perform production capacity analysis
    capacity_analysis = production_capacity_analysis(simulated_plan)
    print("Production Capacity Analysis:")
    print(capacity_analysis)

    # Perform performance analysis
    performance = performance_analysis(simulated_plan)
    print("Performance Analysis:")
    print(performance)

    # Perform quality control
    quality_checked_plan = quality_control(simulated_plan)
    print("Quality Control:")
    print(quality_checked_plan[['code', 'Actual Production', 'Quality Check']])

    # Schedule maintenance
    maintenance_plan = maintenance_schedule(machines)
    print("Maintenance Schedule:")
    print(maintenance_plan)

    # Update human-machine interface status
    hmi_status = human_machine_interface(simulated_plan)
    print("Human-Machine Interface Status:")
    print(hmi_status[['code', 'HMI Status']])

    # MOM intelligence analysis
    mom_intelligence_summary = mom_intelligence(simulated_plan)
    print("MOM Intelligence Analysis:")
    print(mom_intelligence_summary)

    # Save simulated production plan to CSV
    simulated_plan.to_csv('simulated_production_plan.csv', index=False)

if __name__ == "__main__":
    main()
