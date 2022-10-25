from decimal import *


class FinanceYear:
    def __init__(self,
                 initial: Decimal = Decimal(0.0),
                 monthly_salary: Decimal = Decimal(0.0),
                 is_index_salary: bool = False,
                 monthly_expenses: Decimal = Decimal(0.0),
                 is_index_expenses: bool = False,
                 inflation_rate: Decimal = Decimal(0.0),
                 interest_rate: Decimal = Decimal(0.0),
                 devaluation_rate: Decimal = Decimal(1.0),
                 previous_income: Decimal = Decimal(0.0),
                 previous_inflation: Decimal = Decimal(0.0),
                 ):
        self.devaluation_rate = devaluation_rate
        self.initial = initial
        self.monthly_salary = monthly_salary
        self.monthly_expenses = monthly_expenses
        self.is_index_salary = is_index_salary
        self.is_index_expenses = is_index_expenses
        self.inflation_rate = inflation_rate
        self.interest_rate = interest_rate
        self.previous_income = previous_income
        self.previous_inflation = previous_inflation
        self.report = self.generate_report()

    def generate_report(self):
        self.initial += self.monthly_salary * 12
        devaluation_rate = self.devaluation_rate * (1 - (self.inflation_rate * Decimal(0.01)))

        yearly_expenses = self.monthly_expenses * 12
        yearly_salary = self.monthly_salary * 12

        monthly_salary_indexed = self.monthly_salary + (self.monthly_salary * self.inflation_rate * Decimal(0.01))
        yearly_salary_indexed = monthly_salary_indexed * 12
        monthly_expenses_indexed = self.monthly_expenses + (self.monthly_expenses * self.inflation_rate * Decimal(0.01))
        yearly_expenses_indexed = monthly_expenses_indexed * 12


        yearly_income = (self.initial + yearly_salary - yearly_expenses) * (self.interest_rate * Decimal(0.01) + 1)
        monthly_income = yearly_income / 12

        yearly_adjusted_income = yearly_income * self.devaluation_rate
        monthly_adjusted_income = yearly_adjusted_income / 12

        yearly_inflated = (yearly_salary + yearly_income) * (1 - (self.inflation_rate * Decimal(0.01)))
        monthly_inflated = yearly_inflated / 12

        total_income = self.previous_income + yearly_income
        total_adjusted_income = total_income * self.devaluation_rate
        total_inflated = self.previous_inflation + yearly_inflated

        report = {
            "interest_rate": self.interest_rate,
            "inflation_rate": self.inflation_rate,
            "devaluation_rate": devaluation_rate,

            "monthly_salary": monthly_salary_indexed if self.is_index_salary else self.monthly_salary,
            "monthly_expenses": monthly_expenses_indexed if self.is_index_expenses else self.monthly_expenses,

            "yearly_salary": yearly_salary,
            "yearly_expenses": yearly_expenses,

            "monthly_salary_indexed": monthly_salary_indexed,
            "yearly_salary_indexed": yearly_salary_indexed,
            "monthly_expenses_indexed": monthly_expenses_indexed,
            "yearly_expenses_indexed": yearly_expenses_indexed,

            "yearly_income": yearly_income,
            "monthly_income": monthly_income,

            "yearly_adjusted_income": yearly_adjusted_income,
            "monthly_adjusted_income": monthly_adjusted_income,

            "yearly_inflated": yearly_inflated,
            "monthly_inflated": monthly_inflated,

            "total_income": total_income,
            "total_adjusted_income": total_adjusted_income,
            "total_inflated": total_inflated,
        }
        return report


# TODO сделать галочку которая позволит сохранить оригинальное знаечние для годов с for_this_year, если на более ранние года была наложена for_this_and_subsequent
# TODO сделать модалку которая будет уведомлять о том какие года будут затронуты и как именно
# TODO ПРотестировать суммы значений, сопоставить значения с аналогичными сервисами
# TODO Сделать табличку с выводом всех значений, сделать сохранение таблички в csv, excell, сделать загрузку значений обратно в приложение


if __name__ == '__main__':
    inflation_rate = 5
    interest_rate = 10
    monthly_salary = 3000
    monthly_expenses = 1000

    y = FinanceYear(
        inflation_rate=Decimal(inflation_rate),
        interest_rate=Decimal(interest_rate),
        monthly_salary=Decimal(monthly_salary),
        monthly_expenses=Decimal(monthly_expenses),
    )
    from pprint import pprint

    data = y.generate_report()

    data_formatted = {key: round(int(value), 0) for key, value in data.items()}
    pprint(data_formatted)
