from finance_year import FinanceYear
from decimal import Decimal
from enum import Enum
import json
from pprint import pprint


class YearsSpan(Enum):
    THIS_YEAR = '1'
    ALL_SUBSEQUENT = '2'


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

по сути base уровень существует только для первого года,
остальные получают значения по цепоке
"""


def decimal_into_json_float_rounded(obj):
    if isinstance(obj, Decimal):
        return round(float(obj), 2)
    return str(obj)


class PlanComposer:

    def __init__(self):
        self.years = []
        self.years_salary_indexed = set()
        self.years_expenses_indexed = set()

    def add_year(self,
                 monthly_salary: Decimal = None,
                 monthly_expenses: Decimal = None,
                 interest_rate: Decimal = None,
                 inflation_rate: Decimal = None,
                 is_index_salary: bool = False,
                 is_index_expenses: bool = False
                 ) -> FinanceYear:
        """ calculates values for new year, based on previous """

        # TODO сделать автоиндексацию по предыдущему году

        if self.years:
            prev_year = self.years[-1]
            prev_year_report = prev_year.report
            self.years.append(FinanceYear(
                monthly_salary=monthly_salary if monthly_salary is not None else prev_year_report["monthly_salary"],
                monthly_expenses=monthly_expenses if monthly_expenses is not None else prev_year_report[
                    "monthly_expenses"],
                inflation_rate=inflation_rate if inflation_rate is not None else prev_year.inflation_rate,
                interest_rate=interest_rate if interest_rate is not None else prev_year.interest_rate,
                is_index_salary=is_index_salary,
                is_index_expenses=is_index_expenses,
                devaluation_rate=prev_year_report["devaluation_rate"],
                previous_balance=prev_year_report["total_balance"],
                previous_inflation=prev_year_report["total_inflated"]))

        else:
            self.years.append(
                FinanceYear(
                    monthly_salary=monthly_salary if monthly_salary is not None else Decimal(0),
                    monthly_expenses=monthly_expenses if monthly_expenses is not None else Decimal(0),
                    inflation_rate=inflation_rate if inflation_rate is not None else Decimal(0),
                    interest_rate=interest_rate if interest_rate is not None else Decimal(0),
                    is_index_salary=is_index_salary,
                    is_index_expenses=is_index_expenses,
                ))
        return self.years[-1]

    def save_year(self, year_number: int,
                  interest_rate: Decimal = None,
                  inflation_rate: Decimal = None,
                  monthly_salary: Decimal = None,
                  monthly_expenses: Decimal = None,
                  interest_rate_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  inflation_rate_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  monthly_salary_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  monthly_expenses_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  salary_indexing_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  expenses_indexing_span: YearsSpan = YearsSpan.THIS_YEAR.value,
                  is_index_salary: bool = False,
                  is_index_expenses: bool = False,
                  ):
        """apply new values from input, method called on "save" """
        year_index = year_number - 1
        year_prev_state = self.years[year_index]
        if len(self.years) == 1:
            self.years[year_index] = FinanceYear(
                interest_rate=interest_rate if interest_rate is not None else year_prev_state.interest_rate,
                inflation_rate=inflation_rate if inflation_rate is not None else year_prev_state.inflation_rate,
                monthly_salary=monthly_salary if monthly_salary is not None else year_prev_state.monthly_salary,
                monthly_expenses=monthly_expenses if monthly_expenses is not None else year_prev_state.monthly_expenses,
                is_index_salary=is_index_salary if is_index_salary else year_prev_state.is_index_salary,
                is_index_expenses=is_index_expenses if is_index_expenses else year_prev_state.is_index_expenses
            )
        else:
            prev_year = self.years[year_index - 1]
            prev_year_report = prev_year.report
            self.years[year_index] = FinanceYear(
                interest_rate=interest_rate if interest_rate is not None else year_prev_state.interest_rate,
                inflation_rate=inflation_rate if inflation_rate is not None else year_prev_state.inflation_rate,
                monthly_salary=monthly_salary if monthly_salary is not None else year_prev_state.monthly_salary,
                monthly_expenses=monthly_expenses if monthly_expenses is not None else year_prev_state.monthly_expenses,
                is_index_salary=is_index_salary if is_index_salary else year_prev_state.is_index_salary,
                is_index_expenses=is_index_expenses if is_index_expenses else year_prev_state.is_index_expenses,
                devaluation_rate=prev_year_report['devaluation_rate'],
                previous_balance=prev_year_report['total_balance'],
                previous_inflation=prev_year_report['total_inflated'],
            )



"""     for_this_and_subsequent влияет на каждый новый созданный год,

        если новая ЗП и галочка индексации, то индексируем заново
        если старая  ЗП и галочка индексации, без предыдущей индексации - индексируем впервые, и делаем отображение равных обычной и индексированной зп
        если старая ЗП и галочка индексации, и до этого уже была индексация - ничего не делаем, и делаем отображение равных обычной и индексированной зп
        если новая инфляция, галочка индексации, и любая ЗП, то заново расчитываем индексацию, и делаем отображение равных обычной и индексированной зп
        """

        # year = None
        # for i in range(total_years - n):
        #     old_year = old_values[i]
        #
        #     interest_rate = custom_interest_rate if interest_rate_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.interest_rate
        #     inflation_rate = custom_inflation_rate if inflation_rate_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.inflation_rate
        #     monthly_salary = old_year.report[
        #         'monthly_salary'] if monthly_salary_span == YearsSpan.THIS_YEAR.value else custom_monthly_salary if monthly_salary_span == YearsSpan.ALL_SUBSEQUENT.value else \
        #     self.years[-1].report['monthly_salary']
        #     is_index_salary = True if salary_indexing_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.is_index_salary
        #     is_index_expenses = True if expenses_indexing_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.is_index_expenses
        #
        #
        #     year = self.add_year(interest_rate=custom_interest_rate if interest_rate_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.interest_rate,
        #                   inflation_rate=custom_inflation_rate if inflation_rate_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.inflation_rate,
        #                   monthly_salary=old_year.report['monthly_salary'] if monthly_salary_span == YearsSpan.THIS_YEAR.value else custom_monthly_salary if monthly_salary_span == YearsSpan.ALL_SUBSEQUENT.value else self.years[-1].report['monthly_salary'],
        #                   monthly_expenses=old_year.report['monthly_expenses'] if monthly_salary_span == YearsSpan.THIS_YEAR.value else custom_monthly_expenses if monthly_expenses_span == YearsSpan.ALL_SUBSEQUENT.value else self.years[-1].report['monthly_expenses'],
        #                   is_index_salary=True if salary_indexing_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.is_index_salary,
        #                   is_index_expenses=True if expenses_indexing_span == YearsSpan.ALL_SUBSEQUENT.value else old_year.is_index_expenses)
