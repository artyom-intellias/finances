from finance_year import FinanceYear
from decimal import Decimal
from enum import Enum
import json
from pprint import pprint


class YearsIndexing(Enum):
    THIS_YEAR = 1
    ALL_SUBSEQUENT = 2


"""
если к году добавилась галочка for_this_and_subsequent
переписываются все последующий годы с заданным значением и галочкой

если год сохранён с галочкой for_this_year, то у него меняются показатели, а остальные года пересчитываются

если к году добавилась галочка for_this_year на любой из
показателей, тогда меняем значения этого года
в соответствии с флажками, а следующий год получит свои флажки
из предыдущего года, давая текущему исключительное значение
но, если предыдущий год тоже имеет галочку for_this_year,
тогда ищем год в котором её нет, если такой год не найден, сбрасываем до base уровня

если в этом году for_this_year, а в предыдущем была for_this_and_subsequent,
тогда следующий получит значение из for_this_and_subsequent

for_this_and_subsequent влияет на каждый новый созданный год,
по сути base уровень существует только для первого года,
остальные получают значения по цепоке
"""


def decimal_into_json_float_rounded(obj):
    if isinstance(obj, Decimal):
        return round(float(obj), 2)
    return str(obj)


class PlanComposer:

    def __init__(self, monthly_salary, monthly_expenses, interest_rate, inflation_rate, years_total):
        self.years = []

        year = FinanceYear(
            monthly_salary=Decimal(monthly_salary),
            monthly_expenses=Decimal(monthly_expenses),
            interest_rate=Decimal(interest_rate),
            inflation_rate=Decimal(inflation_rate)
        )
        self.years.append(year)
        for i in range(years_total):
            year = self.add_year(year)
            self.years.append(year)

    def save_year(self, n: int, total_years: int,
                  custom_monthly_salary: Decimal = None,
                  custom_monthly_expenses: Decimal = None,
                  custom_interest_rate: Decimal = None,
                  custom_inflation_rate: Decimal = None,
                  salary_indexing_span: YearsIndexing = None,
                  expenses_indexing_span: YearsIndexing = None,
                  interest_rate_indexing_span: YearsIndexing = None,
                  inflation_rate_indexing_span: YearsIndexing = None,
                  ):
        """apply new values from input, method called on "save" """
        self.years = self.years[:n]
        before_save = self.years[n - 1]
        self.years[n - 1] = FinanceYear(
            initial=before_save.initial,
            monthly_salary=custom_monthly_salary if custom_monthly_salary else before_save.monthly_salary,
            monthly_expenses=custom_monthly_expenses if custom_monthly_expenses else before_save.monthly_expenses,
            is_index_salary=True if salary_indexing_span else salary_indexing_span,
            is_index_expenses=True if expenses_indexing_span else expenses_indexing_span,
            interest_rate=custom_interest_rate if custom_interest_rate else before_save.interest_rate,
            inflation_rate=custom_inflation_rate if custom_inflation_rate else before_save.inflation_rate,
            devaluation_rate=before_save.devaluation_rate,
            previous_income=before_save.previous_income,
            previous_inflation=before_save.previous_inflation
        )

        year = self.years[-1]
        for i in range(total_years - n):
            year = self.add_year(year,
                                 custom_interest_rate=custom_interest_rate if interest_rate_indexing_span == YearsIndexing.ALL_SUBSEQUENT else None,
                                 custom_inflation_rate=custom_inflation_rate if inflation_rate_indexing_span == YearsIndexing.ALL_SUBSEQUENT else None,
                                 is_index_salary=True if salary_indexing_span == YearsIndexing.ALL_SUBSEQUENT else False,
                                 is_index_expenses=True if expenses_indexing_span == YearsIndexing.ALL_SUBSEQUENT else False)
            self.years.append(year)

    def add_year(self,
                 monthly_salary: Decimal = None,
                 monthly_expenses: Decimal = None,
                 interest_rate: Decimal = None,
                 inflation_rate: Decimal = None,
                 is_index_salary: bool = False,
                 is_index_expenses: bool = False
                 ) -> FinanceYear:
        """ calculates values for new year, based on previous """

        if self.years:
            prev_year = self.years[-1]
            prev_year_report = prev_year.report

            new_year = FinanceYear(
                monthly_salary=monthly_salary if monthly_salary else prev_year_report["monthly_salary"],
                monthly_expenses=monthly_expenses if monthly_expenses else prev_year_report["monthly_expenses"],
                is_index_salary=is_index_salary,
                is_index_expenses=is_index_expenses,
                inflation_rate=inflation_rate if inflation_rate else prev_year.inflation_rate,
                interest_rate=interest_rate if interest_rate else prev_year.interest_rate,
                devaluation_rate=prev_year_report["devaluation_rate"],
                previous_balance=prev_year_report["total_balance"],
                previous_inflation=prev_year_report["total_inflated"])

            self.years.append(new_year)
            return new_year
        else:
            self.years.append(
                FinanceYear(
                    monthly_salary=monthly_salary,
                    monthly_expenses=monthly_expenses,
                    inflation_rate=inflation_rate,
                    interest_rate=interest_rate
                )
            )
