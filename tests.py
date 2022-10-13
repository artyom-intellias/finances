import pytest
from decimal import *


def year_as_whole(initial, inflation_rate, monthly):
    initial += monthly * 12
    initial *= inflation_rate * 0.01
    return initial


def year_in_separate_months(initial, inflation_rate, monthly):
    monthly_inflation = inflation_rate / 12

    for _ in range(12):
        initial *= monthly_inflation * 0.01
        monthly *= monthly_inflation * 0.01

        initial += monthly



a = year_as_whole(10_000, 5, 2_000)

b = year_in_separate_months(10_000, 5, 2_000)