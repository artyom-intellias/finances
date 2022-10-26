import pytest
from decimal import Decimal
from src.plan_composer import PlanComposer


@pytest.fixture
def empty_plan():
    return PlanComposer()
@pytest.fixture
def one_year_plan(empty_plan):
    empty_plan.add_year(monthly_salary=Decimal(2000), monthly_expenses=Decimal(1000), interest_rate=Decimal(10),
                        inflation_rate=Decimal(10))
    return empty_plan
@pytest.fixture
def three_years_plan(one_year_plan):
    one_year_plan.add()
    one_year_plan.add()
    return one_year_plan
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
    inflation = Decimal(10)

    empty_plan.add_year(monthly_salary=initial_salary, inflation_rate=inflation, is_index_salary=True)
    assert float(empty_plan.years[-1].report['monthly_salary']) == float(11)

    new_inflation = Decimal(20)
    empty_plan.add_year(monthly_salary=initial_salary, inflation_rate=new_inflation, is_index_salary=True)
    assert float(empty_plan.years[-1].report['monthly_salary']) == float(12)
def test_add_index_expenses(empty_plan):
    initial_salary = Decimal(10)
    inflation = Decimal(10)

    empty_plan.add_year(monthly_expenses=initial_salary, inflation_rate=inflation, is_index_expenses=True)
    assert float(empty_plan.years[-1].report['monthly_expenses']) == float(11)

    new_inflation = Decimal(20)
    empty_plan.add_year(monthly_expenses=initial_salary, inflation_rate=new_inflation, is_index_expenses=True)
    assert float(empty_plan.years[-1].report['monthly_expenses']) == float(12)

def test_save_monthly_salary_one_year(three_years_plan):
def test_save_monthly_salary_single(three_years_plan):...
def test_save_monthly_salary_single_indexed(three_years_plan): ...
def test_save_monthly_salary_multi(three_years_plan): ...
def test_save_monthly_salary_multi_indexed(three_years_plan): ...

def test_save_monthly_expenses_single(three_years_plan): ...
def test_save_monthly_expenses_single_indexed(three_years_plan): ...
def test_save_monthly_expenses_multi(three_years_plan): ...
def test_save_monthly_expenses_multi_indexed(three_years_plan): ...

def test_save_inflation_rate_single(three_years_plan): ...
def test_save_inflation_rate_multi(three_years_plan): ...
def test_save_interest_rate_single(three_years_plan): ...
def test_save_interest_rate_multi(three_years_plan): ...
