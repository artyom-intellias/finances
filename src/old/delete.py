from decimal import Decimal


devaluation = 1
base_inf = Decimal(0.05)
interest_rate = 10
initial = 0
initial_non_invested = 0

monthly_salary = 2000
wanted_monthly_income = 3000

expected_lifespan = 60


for i in range(1, 30):
    print(f' year {i}')

    devaluation *= 1 - base_inf
    print(f'{devaluation=:.2f}')
    initial += monthly_salary * 12

    before_profit = initial
    initial_non_invested += monthly_salary * 12
    initial *= 1 + interest_rate * Decimal(0.01)

    pure_profit = initial - before_profit
    pure_profit_monthly = pure_profit / 12
    pure_real_profit = pure_profit * devaluation
    pure_real_profit_monthly = pure_real_profit / 12
    pure_initial_non_invested = initial_non_invested * devaluation

    inflated_yearly = base_inf * initial
    inflated_monthly = inflated_yearly / 12

    print(f"{initial=:.0f} {initial_non_invested=:.0f} {pure_initial_non_invested=:.0f}")
    print(f"{pure_profit=:.0f} {pure_real_profit=:.0f} {pure_profit_monthly=:.0f} {pure_real_profit_monthly=}")
    print(f"{inflated_yearly=:.0f} {inflated_monthly=:.0f}")
    print()

    if pure_real_profit_monthly > wanted_monthly_income:
        print('wow')
        # break
    if inflated_monthly > wanted_monthly_income:
        print('fucking hell!')
        break

