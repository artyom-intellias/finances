import pytest
from decimal import Decimal
from src.plan_composer import PlanComposer


@pytest.fixture
def empty_plan():
    return PlanComposer()


def test_empty(empty_plan):
    assert len(empty_plan.years) == 0


def test_add(empty_plan):
    empty_plan.add_year()
    assert len(empty_plan.years) == 1


def test_add_monthly_salary_consistency(empty_plan):
    empty_plan.add_year(monthly_salary=Decimal(1))
    empty_plan.add_year()
    empty_plan.add_year()
    assert empty_plan.years[-1].report['monthly_salary'] == 1


def test_add_monthly_expenses_consistency(empty_plan):
    empty_plan.add_year(monthly_expenses=Decimal(1))
    empty_plan.add_year()
    empty_plan.add_year()
    assert empty_plan.years[-1].report['monthly_expenses'] == 1


def test_add_interest_rate_consistency(empty_plan):
    empty_plan.add_year(interest_rate=Decimal(1))
    empty_plan.add_year()
    empty_plan.add_year()
    assert empty_plan.years[-1].report['interest_rate'] == 1


def test_add_inflation_rate_consistency(empty_plan):
    empty_plan.add_year(inflation_rate=Decimal(1))
    empty_plan.add_year()
    empty_plan.add_year()
    assert empty_plan.years[-1].report['inflation_rate'] == 1


def test_add_index_salary(empty_plan):
    initial_salary = Decimal(10)
    empty_plan.add_year(monthly_salary=initial_salary, is_index_salary=True)
    assert empty_plan.years[-1].report['monthly_salary'] == initial_salary

    inflation = Decimal(10)
    empty_plan.add_year(monthly_salary=initial_salary, inflation_rate=inflation, is_index_salary=True)
    assert float(empty_plan.years[-1].report['monthly_salary']) == float(11)


def test_add_index_expenses(empty_plan):
    initial_expenses = Decimal(10)
    empty_plan.add_year(monthly_expenses=initial_expenses, is_index_expenses=True)
    assert empty_plan.years[-1].report['monthly_expenses'] == initial_expenses

    inflation = Decimal(10)
    empty_plan.add_year(monthly_expenses=initial_expenses, inflation_rate=inflation, is_index_expenses=True)
    assert float(empty_plan.years[-1].report['monthly_expenses']) == float(11)
