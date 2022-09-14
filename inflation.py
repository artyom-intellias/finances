class Calc:

    def __init__(self, initial=0, monthly=0, perc_avg=0.0, years=0, recursive_pay=False):
        self.initial = initial  # начальная сума вклада
        self.monthly = monthly  # ежемесячное зачисление
        self.perc_avg = perc_avg  # средняя норма прибыли после инфляции
        self.years = years  # количество лет
        self.recursive_pay = recursive_pay  # возвращаются ли обратно дивиденты на вклад?

    def generate_report(self, recursive_payments=False):
        report = []
        amount = 0
        if self.initial:
            amount += self.initial
            report.append(f"Начальный вклад {self.initial=}")
        for year in range(1, self.years + 1):
            amount += self.monthly * 12
            year_perc_income = amount * self.perc_avg * 0.01
            amount += year_perc_income
            if recursive_payments:
                report.append(
                    f"Год {year}, сумма c реинвестированием дивидендов {amount:.0f}, проценты {year_perc_income:.2f} (ежемесячно {year_perc_income / 12:.2f})")
            else:
                report.append(
                    f"Год {year}, сумма {amount}, проценты {year_perc_income} (ежемесячно {year_perc_income / 12:.2f})")
        return report

    def print_report(self):
        for record in self.generate_report():
            print(record)

        for record in self.generate_report(recursive_payments=True):
            print(record)


if __name__ == '__main__':
    Calc(
        initial=int(input('Введи начальную сумму инвестиций\n')),
        monthly=int(input('Введи ежемесячный вклад\n')),
        perc_avg=float(input('Введи ежегодный процент прибыли\n')),
        years=int(input('Введи количество лет в течении которых будут откладываться деньги\n')),
    ).print_report()


	# начальный вклад 40000, ежемесячный вклад 3000, норма прибыли 7% на 3 года, с реинвестированием = 172840
	# начальный вклад 172840 ежемесячный вклад 3500, норма прибыли 7% на 3 года, с реинвестированием = 356214
	# начальный вклад 356214, ежемесячный вклад 4000, норма прибыли 7% на 4 года, с реинвестированием = 694959

	# конец активной фазы накопления, вкладываем только дивиденды
	# начальный вклад 694959, ежемесячный вклад 4000, норма прибыли 7% на 10 лет, с реинвестированием = 2076702