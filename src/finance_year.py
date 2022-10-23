from decimal import *


class FinanceYear:
    def __init__(self,
                 initial: Decimal or float = 0.0,
                 monthly_salary: Decimal or float = 0.0,
                 index_salary: bool = False,
                 living_cost: Decimal or float = 0.0,
                 index_living_cost: bool = False,
                 inflation_rate: Decimal or float = 0.0,
                 interest_rate: Decimal or float = 0.0,
                 devaluation_rate: Decimal or float = 1.0,
                 previous_income: Decimal or float = 1.0,
                 previous_inflation: Decimal or float = 1.0,
                 ):
        self.devaluation_rate = Decimal(Decimal(devaluation_rate) * (1 - (Decimal(inflation_rate) * Decimal(0.01))))
        self.initial = Decimal(initial)
        self.monthly_salary = Decimal(monthly_salary)
        self.index_salary = Decimal(index_salary)
        self.living_cost = Decimal(living_cost)
        self.index_living_cost = Decimal(index_living_cost)
        self.inflation_rate = Decimal(inflation_rate)
        self.interest_rate = Decimal(interest_rate)
        self.previous_income = Decimal(previous_income)
        self.previous_inflation = Decimal(previous_inflation)
        self.report = self.generate_report()

    def generate_report(self):
        self.initial += self.monthly_salary * 12
        yearly_salary = self.monthly_salary * 12
        yearly_living_cost = self.living_cost * 12
        monthly_salary_indexed = self.monthly_salary + (self.monthly_salary * self.inflation_rate * Decimal(0.01))
        yearly_salary_indexed = monthly_salary_indexed * 12
        monthly_living_cost_indexed = self.living_cost + (self.living_cost * self.inflation_rate * Decimal(0.01))
        yearly_living_cost_indexed = monthly_living_cost_indexed * 12
        yearly_income = (self.initial + yearly_salary) * (self.interest_rate * Decimal(0.01) + 1)
        monthly_income = yearly_income / 12
        yearly_adjusted_income = yearly_income * self.devaluation_rate
        monthly_adjusted_income = yearly_adjusted_income / 12
        yearly_inflated = (yearly_salary + yearly_income) * (1 - (self.inflation_rate * Decimal(0.01)))
        monthly_inflated = yearly_inflated / 12
        total_income = self.previous_income + yearly_income
        total_adjusted_income = total_income * self.devaluation_rate
        total_inflated = self.previous_inflation + yearly_inflated

        report = {
            "devaluation_rate": self.devaluation_rate,
            "yearly_salary": yearly_salary,
            "yearly_living_cost": yearly_living_cost,
            "monthly_salary_indexed": monthly_salary_indexed,
            "yearly_salary_indexed": yearly_salary_indexed,
            "monthly_living_cost_indexed": monthly_living_cost_indexed,
            "yearly_living_cost_indexed": yearly_living_cost_indexed,
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


"""

если к году добавилась галочка for_this_and_subsequent переписываются все последующий годы с заданным значением и галочкой

если к году добавилась галочка for_this_year на любой из показателей, тогда меняем значения этого года
в соответствии с флажками, а следующий год получит свои флажки из предыдущего года, давая текущему исключительное значение
но, если предыдущий год тоже имеет галочку for_this_year, тогда ищем год в котором её нет, если такой год не найден, сбрасываем до base уровня

если в этом году for_this_year, а в предыдущем была for_this_and_subsequent, тогда следующий получит значение из for_this_and_subsequent

for_this_and_subsequent влияет на каждый новый созданный год, по сути base уровень существует только для первого года, остальные получают значения по цепоке
"""

# TODO сделать галочку которая позволит сохранить оригинальное знаечние для годов с for_this_year, если на более ранние года была наложена for_this_and_subsequent
# TODO сделать модалку которая будет уведомлять о том какие года будут затронуты и как именно
# TODO ПРотестировать суммы значений, сопоставить значения с аналогичными сервисами
# TODO Сделать табличку с выводом всех значений, сделать сохранение таблички в csv, excell, сделать загрузку значений обратно в приложение


if __name__ == '__main__':
    base_inf = 10
    y = FinanceYear(inflation_rate=base_inf)
    print(y.devaluation_rate)
    acc = y.devaluation_rate
    for i in range(4):
        y = FinanceYear(inflation_rate=base_inf, devaluation_rate=acc)
        acc = y.devaluation_rate
        print(y.devaluation_rate)
