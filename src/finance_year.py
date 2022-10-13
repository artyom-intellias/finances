from decimal import *


class FinanceYear:
    def __init__(self, initial: Decimal = 0.0, monthly_salary: Decimal = 0.0, inflation_rate: Decimal = 0.0,
                 interest_rate: Decimal = 0.0):
        self.initial = initial
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
