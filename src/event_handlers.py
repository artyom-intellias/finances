from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event, validate_number_input, set_base_param
from plan_composer import PlanComposer
import js
from decimal import Decimal


def populate_year_form(year_number=0, year_info=None):
    trim_decimal = lambda x: float(round(x, 0))

    def set_info_by_id(id_, key, input=False):
        value = trim_decimal(year_info.report[key]) if year_info else 0
        if input:
            js.document.getElementById(id_).value = value
        else:
            js.document.getElementById(id_).textContent = value

    js.document.getElementById("year_number").textContent = f"Year #{year_number}"

    set_info_by_id('monthly_salary_detailed_input', 'monthly_salary', input=True)
    set_info_by_id('yearly_salary', 'yearly_salary')
    set_info_by_id('monthly_salary_indexed', 'monthly_salary_indexed')
    set_info_by_id('yearly_salary_indexed', 'yearly_salary_indexed')

    set_info_by_id('monthly_expenses_detailed_input', 'monthly_expenses', input=True)
    set_info_by_id('yearly_expenses', 'yearly_expenses')
    set_info_by_id('monthly_expenses_indexed', 'monthly_expenses_indexed')
    set_info_by_id('yearly_expenses_indexed', 'yearly_expenses_indexed')

    set_info_by_id('interest_rate_detailed_input', 'interest_rate', input=True)
    set_info_by_id('yearly_income', 'yearly_income')
    set_info_by_id('yearly_adjusted_income', 'yearly_adjusted_income')
    set_info_by_id('monthly_income', 'monthly_income')
    set_info_by_id('monthly_adjusted_income', 'monthly_adjusted_income')
    set_info_by_id('total_income', 'total_income')

    set_info_by_id('inflation_rate_detailed_input', 'inflation_rate', input=True)
    set_info_by_id('monthly_inflated', 'monthly_inflated')
    set_info_by_id('total_inflated', 'total_inflated')


def e_year_btn(e):
    active_year_id = js.document.getElementById('year_btn_active').title
    if active_year_id:
        year_el = js.document.getElementById(active_year_id)
        if active_year_id == e.target.id:
            pass
        else:
            year_el.classList.remove('active')
            e.target.classList.add('active')
            js.document.getElementById('year_btn_active').title = e.target.id

    else:
        e.target.classList.add('active')
        js.document.getElementById('year_btn_active').title = e.target.id

    active_year_id_updated = js.document.getElementById('year_btn_active').title
    year_number = int(active_year_id_updated[5:])
    info_index = year_number - 1
    year_info = js.document.plan.years[info_index]
    populate_year_form(year_number, year_info)


def e_prev_year_btn(e):
    active_year_id = int(js.document.getElementById('year_btn_active').title.split('_')[1])

    years_list = js.document.getElementById("years_list")
    years_total = years_list.childElementCount + 1
    if years_total == 1 and active_year_id == 1:
        return

    prev_year = js.document.getElementById(f'year_{active_year_id - 1}')
    if prev_year:
        prev_year.click()


def e_next_year_btn(e):
    active_year_id = int(js.document.getElementById('year_btn_active').title.split('_')[1])

    years_list = js.document.getElementById("years_list")
    years_total = years_list.childElementCount + 1
    if years_total == 1 and active_year_id == 1:
        return

    next_year = js.document.getElementById(f'year_{active_year_id + 1}')
    if next_year:
        next_year.click()


def e_add_year(e):
    years_list = js.document.getElementById("years_list")
    years_total = years_list.childElementCount + 1
    years_count = js.document.getElementById("years_stored_value")
    years_count.textContent = years_total

    year_btn = create_el('button', id_=f"year_{years_total}",
                         class_="btn btn-light col list-group-item sortable-item border year-list-item-btn p-3",
                         custom={"type": "button"})
    btn_text = create_el(type_='span', class_="text-center muted-event-child", text=f"Year #{years_total}")

    year_btn.appendChild(btn_text)
    years_list.appendChild(year_btn)

    last_year = js.document.plan.years[-1]
    js.document.plan.add_year(prev_year=last_year)

    js.document.getElementById(f"year_{years_total}").onclick = e_year_btn
    js.document.getElementById(f"year_{years_total}").click()


def e_remove_year(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount - 1
    if years_total == 0:
        return

    years_count = js.document.getElementById("years_stored_value")
    years_count.innerText = years_total

    if el.lastChild.classList.contains("active"):
        el.lastChild.previousSibling.classList.add("active")
        js.document.getElementById('year_btn_active').title = el.lastChild.previousSibling.id

    if el.lastChild:
        js.document.plan.years.pop()
        return el.lastChild.remove()
    else:
        return None


def e_set_years(e):
    years_desired = validate_number_input(js.document.getElementById("years_input"), 100, min=1)
    js.document.getElementById("years_input").value = ''
    if not years_desired:
        return None
    el = js.document.getElementById("years_list")
    years_amount = str(el.childElementCount)

    if years_desired > years_amount:
        while years_amount < years_desired:
            trigger_event(e_add_year)
            years_amount = str(el.childElementCount)
    elif years_desired < years_amount:
        while years_amount > years_desired:
            trigger_event(e_remove_year)
            years_amount = str(el.childElementCount)
    else:
        pass


def e_set_monthly_salary(e):
    set_base_param('monthly_salary_stored_value', 'monthly_salary_input', '$', max=100_000, min=1)


def e_set_monthly_expenses(e):
    set_base_param('monthly_expenses_stored_value', 'monthly_expenses_input', '$', max=100_000)


def e_set_base_interest_rate(e):
    set_base_param('base_interest_rate_stored_value', 'base_interest_rate_input', '%', max=100)


def e_set_base_inflation_rate(e):
    set_base_param('base_inflation_rate_stored_value', 'base_inflation_rate_input', '%', max=1000)


js.document.getElementById("add_year_btn").onclick = e_add_year
js.document.getElementById("remove_year_btn").onclick = e_remove_year
js.document.getElementById("set_years_btn").onclick = e_set_years
js.document.getElementById("set_monthly_salary_btn").onclick = e_set_monthly_salary
js.document.getElementById("set_monthly_expenses_btn").onclick = e_set_monthly_expenses
js.document.getElementById("set_base_interest_rate_btn").onclick = e_set_base_interest_rate
js.document.getElementById("set_base_inflation_rate_btn").onclick = e_set_base_inflation_rate
js.document.getElementById("prev_year_btn").onclick = e_prev_year_btn
js.document.getElementById("next_year_btn").onclick = e_next_year_btn
