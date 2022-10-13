from collections import namedtuple
from decimal import *

import plotly.graph_objects as go
from tabulate import tabulate
from dataclasses import dataclass


class FinanceYear:
    def __init__(self, initial: Decimal = 0.0, monthly_salary: Decimal = 0.0, inflation_rate: Decimal = 0.0, interest_rate: Decimal = 0.0):
        self.initial = initial
        self.monthly_salary = monthly_salary
        self.inflation_rate = inflation_rate
        self.interest_rate = interest_rate

    def report(self):
        return {

            'profit'
            'loss'
            ''
        }

    def _process(self):
        if self.initial:
            self.monthly_salary * 12
        self.initial = self.monthly_salary * 12


class Calc:

    def __init__(self, initial=0, monthly_salary=0, perc_avg=0.0, years=0):
        self.initial = initial  # начальная сума вклада
        self.monthly_salary = monthly_salary  # ежемесячное зачисление
        self.perc_avg = perc_avg  # средняя норма прибыли после инфляции
        self.years = years  # количество лет
        self.year_report = namedtuple('year_report',
                                      ['year', 'amount', 'compound_interest_amount', 'inflated_amount',
                                       'year_perc_income', 'year_compound_income', 'year_perc_inflation',
                                       'profit_total', 'compound_profit_total', 'inflation_total'
                                       ])

    def report_graph(self, report):
        fig = go.Figure()

        # main characteristics
        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.amount for year_report in report],
            name='amount',
            marker_color='#FECB52'
        ))
        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.compound_interest_amount for year_report in report],
            name='compound_interest_amount',
            marker_color='chartreuse'
        ))
        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.inflated_amount for year_report in report],
            name='inflated_amount',
            marker_color='#EF553B'
        ))

        # Totals

        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.profit_total for year_report in report],
            name='profit_total',
            marker_color='#FECB52'
        ))
        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.compound_profit_total for year_report in report],
            name='compound_profit_total',
            marker_color='chartreuse'
        ))
        fig.add_trace(go.Bar(
            x=[year_report.year for year_report in report],
            y=[year_report.inflation_total for year_report in report],
            name='inflation_total',
            marker_color='#EF553B'
        ))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        fig.show()

    def report_table(self, report):
        col_names = ['Year', 'amount', 'compound_interest_amount', 'inflated_amount', 'year_perc_income',
                     'year_compound_income', 'year_perc_inflation']
        data = [(r.year, r.amount, r.compound_interest_amount, r.inflated_amount, r.year_perc_income,
                 r.year_compound_income, r.year_perc_inflation) for r in report]
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

        col_names = ['profit_total', 'compound_profit_total', 'inflation_total']
        data = [(r.profit_total, r.compound_profit_total, r.inflation_total) for r in
                [report[-1]]]  # get totals from last
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

        col_names = ['compound_profit_total_perc_from_amount', 'inflation_total_perc_from_amount']
        data1 = [report[-1].compound_interest_amount, report[-1].inflated_amount]
        data2 = [report[-1].compound_profit_total, report[-1].inflation_total]
        data = [[int(data2[0] / (data1[0] * 0.01)), int(data2[1] / (data1[1] * 0.01))]]
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

    def generate_report(self, graph=False, table=False):
        report = []
        amount, compound_interest_amount, inflated_amount, profit_total, compound_profit_total, inflation_total = [
                                                                                                                      0] * 6

        if self.initial:
            amount, compound_interest_amount, inflated_amount = [self.initial] * 3

        for year in range(1, self.years + 1):
            amount += self.monthly_salary * 12
            compound_interest_amount += self.monthly_salary * 12
            inflated_amount += self.monthly_salary * 12

            year_perc_income = amount * self.perc_avg * 0.01
            year_compound_income = compound_interest_amount * self.perc_avg * 0.01
            year_perc_inflation = inflated_amount * self.perc_avg * 0.01

            compound_interest_amount += year_compound_income
            inflated_amount -= year_perc_inflation

            profit_total += year_perc_income
            compound_profit_total += year_compound_income
            inflation_total += year_perc_inflation

            year_report = self.year_report(year=int(year), amount=int(amount),
                                           compound_interest_amount=int(compound_interest_amount),
                                           inflated_amount=int(inflated_amount), year_perc_income=int(year_perc_income),
                                           year_compound_income=int(year_compound_income),
                                           year_perc_inflation=int(year_perc_inflation),
                                           profit_total=int(profit_total),
                                           compound_profit_total=int(compound_profit_total),
                                           inflation_total=int(inflation_total)
                                           )

            report.append(year_report)

        if graph:
            self.report_graph(report)
        if table:
            self.report_table(report)

        return report

    def print_report(self):
        for record in self.generate_report():
            print(record)


if __name__ == '__main__':
    Calc(
        initial=10000,
        monthly_salary=10000,
        perc_avg=10,
        years=5,
    ).generate_report(table=True, graph=True)

# начальный вклад 40000, ежемесячный вклад 3000, норма прибыли 7% на 3 года, с реинвестированием = 172840
# начальный вклад 172840 ежемесячный вклад 3500, норма прибыли 7% на 3 года, с реинвестированием = 356214
# начальный вклад 356214, ежемесячный вклад 4000, норма прибыли 7% на 4 года, с реинвестированием = 694959

# конец активной фазы накопления, вкладываем только дивиденды
# начальный вклад 694959, ежемесячный вклад 4000, норма прибыли 7% на 10 лет, с реинвестированием = 2076702

# todo расчитать когда начать тратить чтоб выйти в ноль

# todo сделать возможность периодизации по годам, для разных фаз накопления с разной активностью

# todo сделать коррекцию на эквивалент сегодняшний и конечной даты

# todo сделать разную инфляцию и ставку snp
