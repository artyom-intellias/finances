
devaluation = 1


base_inf = 0.02
acc = 0
acc_non_invested = 0
interest_rate = 2
monthly_salary = 3000

for i in range(20):
    print(f' year {i}')

    devaluation *= 1 - base_inf
    print(f'{devaluation=:.2f}')
    acc += monthly_salary * 12

    before_divs = acc
    acc_non_invested += monthly_salary * 12
    acc *= 1 + interest_rate * 0.01

    pure_profit = acc - before_divs
    pure_profit_monthly = pure_profit /12
    pure_real_profit = pure_profit * devaluation
    pure_real_profit_monthly = pure_real_profit / 12
    pure_acc_non_invested = acc_non_invested * devaluation
    print(f"{acc_non_invested=}")
    print(f"{acc=}")
    print(f"{pure_profit=}")
    print(f"{pure_real_profit=}")
    print(f"{pure_acc_non_invested=}")
    print(f"{acc=}")
    print(f"{pure_profit_monthly=}")
    print(f"{pure_real_profit_monthly=}")
    print()

real_profit = acc * devaluation
acc_non_invested_and_inflated = acc_non_invested * devaluation


print(f'{devaluation}')
print(f'{acc=:.2f} {real_profit=:.2f}')
print(f'{acc_non_invested=:.2f} {acc_non_invested_and_inflated=:.2f}')
