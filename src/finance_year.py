from decimal import *


class FinanceYear:
    def __init__(self, initial: Decimal = 0.0, monthly_salary: Decimal or float = 0.0, inflation_rate: Decimal or float = 0.0,
                 interest_rate: Decimal or float = 0.0, devaluation_rate: Decimal or float = 1.0):
        self.initial = initial
        self.devaluation_rate = devaluation_rate * (1 - (inflation_rate * 0.01))
        self.monthly_salary = monthly_salary
        self.inflation_rate = inflation_rate
        self.interest_rate = interest_rate

    def _process(self):

        self.initial += self.monthly_salary * 12

        if self.interest_rate > self.inflation_rate:
            diff = self.interest_rate - self.inflation_rate
            self.initial += (self.initial / 100) * diff
        elif self.interest_rate < self.inflation_rate:
            diff = self.inflation_rate - self.interest_rate
            self.initial -= (self.initial / 100) * diff
        else:
            pass

    def net_worth(self) -> float:
        self._process()
        return self.initial


if __name__ == '__main__':
    base_inf = 10
    y = FinanceYear(inflation_rate=base_inf)
    print(y.devaluation_rate)
    acc = y.devaluation_rate
    for i in range(4):
        y = FinanceYear(inflation_rate=base_inf, devaluation_rate=acc)
        acc = y.devaluation_rate
        print(y.devaluation_rate)