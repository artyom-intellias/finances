from finance_year import FinanceYear
from decimal import Decimal
from enum import Enum


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


class PlanComposer:

    def __init__(self, monthly_salary, monthly_expenses, interest_rate, inflation_rate, years_total):
        self.years = []

        year = FinanceYear(
            monthly_salary=monthly_salary,
            monthly_expenses=monthly_expenses,
            interest_rate=interest_rate,
            inflation_rate=inflation_rate
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

    def add_year(self, prev_year: FinanceYear,
                 custom_interest_rate: Decimal = None,
                 custom_inflation_rate: Decimal = None,
                 is_index_salary: bool = False,
                 is_index_expenses: bool = False
                 ) -> FinanceYear:
        """ calculates values for new year, based on previous """
        base_year = prev_year.generate_report()

        new_year = FinanceYear(
            initial=base_year["total_income"],
            monthly_salary=base_year["monthly_salary"],
            monthly_expenses=base_year["monthly_expenses"],
            is_index_salary=is_index_salary,
            is_index_expenses=is_index_expenses,
            inflation_rate=custom_inflation_rate if custom_inflation_rate else base_year["inflation_rate"],
            interest_rate=custom_interest_rate if custom_interest_rate else base_year["interest_rate"],
            devaluation_rate=base_year["devaluation_rate"],
            previous_income=base_year["previous_income"],
            previous_inflation=base_year["previous_inflation"]
        )
        return new_year
