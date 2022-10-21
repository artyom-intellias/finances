
profit = 0
inflated_profit = 0
inflation_rate = 5
profit_rate = 8
acc = 100


for i in range(10):
    profit += 1 + profit_rate * 0.01

    inflated_profit += profit - ((profit * 0.01) * inflation_rate)

    print(f'{profit=}')
    print(f'{inflated_profit=}')
    print()
