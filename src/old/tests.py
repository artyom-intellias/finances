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
def two_years_plan(one_year_plan):
    one_year_plan.add_year()
    return one_year_plan

@pytest.fixture
def three_years_plan(two_years_plan):
    two_years_plan.add_year()
    return two_years_plan

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

def test_save_single_year_plan(one_year_plan):
    year_number = 1
    plan = one_year_plan
    plan.save_year(year_number, monthly_salary=Decimal(3000))
    assert not plan.years[-1].monthly_salary == Decimal(2000)
    assert not plan.years[-1].report['monthly_salary'] == Decimal(2000)
    assert plan.years[-1].monthly_salary == Decimal(3000)
    assert plan.years[-1].report['monthly_salary'] == Decimal(3000)

    plan.save_year(year_number, monthly_expenses=Decimal(500))
    assert not plan.years[-1].monthly_expenses == Decimal(2000)
    assert not plan.years[-1].report['monthly_expenses'] == Decimal(2000)
    assert plan.years[-1].monthly_expenses == Decimal(500)
    assert plan.years[-1].report['monthly_expenses'] == Decimal(500)

    plan.save_year(year_number, inflation_rate=Decimal(50))
    assert not plan.years[-1].inflation_rate == Decimal(2000)
    assert not plan.years[-1].report['inflation_rate'] == Decimal(2000)
    assert plan.years[-1].inflation_rate == Decimal(50)
    assert plan.years[-1].report['inflation_rate'] == Decimal(50)

    plan.save_year(year_number, interest_rate=Decimal(50))
    assert not plan.years[-1].interest_rate == Decimal(2000)
    assert not plan.years[-1].report['interest_rate'] == Decimal(2000)
    assert plan.years[-1].interest_rate == Decimal(50)
    assert plan.years[-1].report['interest_rate'] == Decimal(50)

    plan.save_year(year_number, is_index_salary=True)
    assert not plan.years[-1].is_index_salary == False
    assert not plan.years[-1].report['salary_was_indexed'] == False
    assert plan.years[-1].is_index_salary == True
    assert plan.years[-1].report['salary_was_indexed'] == True
    assert not plan.years[-1].report['monthly_salary'] == Decimal(3000)
    assert not plan.years[-1].report['monthly_salary_indexed'] == Decimal(3000)
    assert float(plan.years[-1].report['monthly_salary_indexed']) == float(4500)
    assert float(plan.years[-1].report['monthly_salary']) == float(4500)

    plan.save_year(year_number, is_index_expenses=True)
    assert not plan.years[-1].is_index_expenses == False
    assert not plan.years[-1].report['expenses_was_indexed'] == False
    assert plan.years[-1].is_index_expenses == True
    assert plan.years[-1].report['expenses_was_indexed'] == True
    assert not plan.years[-1].report['monthly_expenses'] == Decimal(3000)
    assert not plan.years[-1].report['monthly_expenses_indexed'] == Decimal(3000)
    assert float(plan.years[-1].report['monthly_expenses_indexed']) == float(750)
    assert float(plan.years[-1].report['monthly_expenses']) == float(750)


def test_save_two_years_plan_second_year(two_years_plan):
    year_number = 2
    plan = two_years_plan
    plan.save_year(year_number, monthly_salary=Decimal(3000))
    assert not plan.years[-1].monthly_salary == Decimal(2000)
    assert not plan.years[-1].report['monthly_salary'] == Decimal(2000)
    assert plan.years[-1].monthly_salary == Decimal(3000)
    assert plan.years[-1].report['monthly_salary'] == Decimal(3000)

    plan.save_year(year_number, monthly_expenses=Decimal(3000))
    assert not plan.years[-1].monthly_expenses == Decimal(2000)
    assert not plan.years[-1].report['monthly_expenses'] == Decimal(2000)
    assert plan.years[-1].monthly_expenses == Decimal(3000)
    assert plan.years[-1].report['monthly_expenses'] == Decimal(3000)

    plan.save_year(year_number, inflation_rate=Decimal(50))
    assert not plan.years[-1].inflation_rate == Decimal(2000)
    assert not plan.years[-1].report['inflation_rate'] == Decimal(2000)
    assert plan.years[-1].inflation_rate == Decimal(50)
    assert plan.years[-1].report['inflation_rate'] == Decimal(50)

    plan.save_year(year_number, interest_rate=Decimal(50))
    assert not plan.years[-1].interest_rate == Decimal(2000)
    assert not plan.years[-1].report['interest_rate'] == Decimal(2000)
    assert plan.years[-1].interest_rate == Decimal(50)
    assert plan.years[-1].report['interest_rate'] == Decimal(50)

    plan.save_year(year_number, is_index_salary=True)
    assert not plan.years[-1].is_index_salary == False
    assert not plan.years[-1].report['salary_was_indexed'] == False
    assert plan.years[-1].is_index_salary == True
    assert plan.years[-1].report['salary_was_indexed'] == True
    assert not plan.years[-1].report['monthly_salary'] == Decimal(3000)
    assert not plan.years[-1].report['monthly_salary_indexed'] == Decimal(3000)
    assert float(plan.years[-1].report['monthly_salary_indexed']) == float(4500)
    assert float(plan.years[-1].report['monthly_salary']) == float(4500)

    plan.save_year(year_number, is_index_expenses=True)
    assert not plan.years[-1].is_index_expenses == False
    assert not plan.years[-1].report['expenses_was_indexed'] == False
    assert plan.years[-1].is_index_expenses == True
    assert plan.years[-1].report['expenses_was_indexed'] == True
    assert not plan.years[-1].report['monthly_expenses'] == Decimal(3000)
    assert not plan.years[-1].report['monthly_expenses_indexed'] == Decimal(3000)
    assert float(plan.years[-1].report['monthly_expenses_indexed']) == float(4500)
    assert float(plan.years[-1].report['monthly_expenses']) == float(4500)





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
