import numpy as np
import pandas as pd

# Function to read data from CSV
def read_data(file_path):
    data = pd.read_csv(file_path, delimiter=';')
    return data

# Wagner-Whitin Function
def wagner_whitin(demand, setup_cost, holding_cost):
    n = len(demand)
    cost = np.zeros((n, n))
    for i in range(n):
        cost[i, i] = demand[i] * holding_cost

    for i in range(n):
        for j in range(i + 1, n):
            cost[i, j] = cost[i, j - 1] + demand[j] * holding_cost

    dp = [0] * n
    dp[0] = cost[0, 0]
    for j in range(1, n):
        dp[j] = min([dp[i - 1] + cost[i, j] + setup_cost for i in range(j + 1)])

    return dp[-1]

# Main function
def main():
    # Read data from CSV
    file_path = 'demand_forecasts.csv'
    data = read_data(file_path)

    demand = data['forecast'].tolist()
    setup_cost = 500
    holding_cost = 1

    total_cost = wagner_whitin(demand, setup_cost, holding_cost)
    print(f"Total Cost: {total_cost}")

    # Forward Calculation
    data_calc = data.copy()

    for i in data_calc['period'].unique():
        data_calc['Order {}'.format(i)] = 0

    # Costs
    set_up = 500
    holding = 1

    # Order 1
    order = 1
    for index, row in data_calc.iterrows():
        current_month = data_calc.loc[index, 'period']
        cost = 0
        # 1 set up
        cost += set_up
        if current_month > 1:
            for t in range(1, current_month + 1):
                cost += (t - 1) * data_calc.loc[t - 1, 'forecast'] * holding
        data_calc.loc[index, 'Order {}'.format(order)] = cost

    # Orders 2 to 12
    for order in range(2, 13):
        for index, row in data_calc.iterrows():
            current_month = data_calc.loc[index, 'period']
            if current_month >= order:
                cost = 0

                # Best option best Period 1
                values = list(data_calc.loc[order - 2, ['Order {}'.format(i) for i in range(1, order + 1)]].values)
                best = min([i for i in values if i > 0])

                # Add
                cost += best + set_up
                for t in range(order, current_month + 1):
                    cost += (t - order) * data_calc.loc[t - 1, 'forecast'] * holding
                data_calc.loc[index, 'Order {}'.format(order)] = cost

    data_calc = data_calc.set_index('period').drop(['forecast'], axis=1).T
    print(data_calc)

    # Backward Calculation
    costs, initials, nexts, quantities = [], [], [], []
    i = 12
    while i > 1:
        # Order with the minimum cost
        initial_step = i
        next_step = data_calc[data_calc[i] > 0][i].idxmin()
        cost = data_calc[data_calc[i] > 0][i].min()
        # Next Step
        next_id = int(next_step.replace('Order ', ''))
        i = next_id - 1
        # Quantity
        quantity = data[data['period'].isin(range(next_id, initial_step + 1))]['forecast'].sum()

        costs.append(cost)
        initials.append(initial_step)
        nexts.append(next_id)
        quantities.append(quantity)

    df_results = pd.DataFrame({'backward': range(1, len(initials) + 1),
                               'initial': initials,
                               'nexts': nexts,
                               'cost': costs,
                               'quantity': quantities}).set_index('backward')
    print("Total Cost: {:,}$".format(df_results.cost.sum()))
    print(df_results)

if __name__ == "__main__":
    main()
