from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event, validate_number_input, set_base_param, populate_year_form
from plan_composer import PlanComposer
import js
from decimal import Decimal

js.document.active_year = 0
js.document.plan = PlanComposer()


def e_year_btn(e):
    active_year_id = js.document.active_year

    if active_year_id:
        year_el = js.document.getElementById(f'year_{active_year_id}')
        if active_year_id == e.target.id:
            pass
        else:
            year_el.classList.remove('active')
            e.target.classList.add('active')
            js.document.active_year = int(e.target.id.split('_')[1])
    else:
        e.target.classList.add('active')
        js.document.getElementById('year_btn_active').title = e.target.id
        js.document.active_year = int(e.target.id.split('_')[1])

    # fill with calculated data
    active_year_id = js.document.active_year
    year_info = js.document.plan.years[active_year_id - 1]
    populate_year_form(active_year_id, year_info)


def e_prev_year_btn(e):
    active_year_id = js.document.active_year

    years_list = js.document.getElementById("years_list")
    years_total = years_list.childElementCount
    if years_total:
        if years_total == 1 and active_year_id == 1:
            return

        prev_year = js.document.getElementById(f'year_{active_year_id - 1}')
        if prev_year:
            prev_year.click()


def e_next_year_btn(e):
    active_year_id = js.document.active_year
    if active_year_id:
        next_year = js.document.getElementById(f'year_{active_year_id + 1}')
        if next_year:
            next_year.click()


def e_add_year(e):
    # update counters
    years_list = js.document.getElementById("years_list")
    years_present = years_list.childElementCount + 1
    years_counter = js.document.getElementById("years_stored_value")
    years_counter.textContent = years_present

    # create year button
    year_btn = create_el('button', id_=f"year_{years_present}",
                         class_="btn btn-light col list-group-item sortable-item border year-list-item-btn p-3",
                         custom={"type": "button"})
    btn_text = create_el(type_='span', class_="text-center muted-event-child", text=f"Year #{years_present}")
    year_btn.appendChild(btn_text)
    years_list.appendChild(year_btn)

    if not js.document.plan.years:

        monthly_salary = Decimal(js.document.getElementById("monthly_salary_stored_value").innerText[:-2])
        monthly_expenses = Decimal(js.document.getElementById("monthly_expenses_stored_value").innerText[:-2])
        interest_rate = Decimal(js.document.getElementById("base_interest_rate_stored_value").innerText[:-2])
        inflation_rate = Decimal(js.document.getElementById("base_inflation_rate_stored_value").innerText[:-2])
        js.document.plan.add_year(monthly_salary=monthly_salary,
                                  monthly_expenses=monthly_expenses,
                                  interest_rate=interest_rate,
                                  inflation_rate=inflation_rate)
    else:
        js.document.plan.add_year()

    # toggle new year to "active" state, and update year tab
    js.document.getElementById(f"year_{years_present}").onclick = e_year_btn
    js.document.getElementById(f"year_{years_present}").click()


def e_remove_year(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount
    if not years_total:
        return None
    elif years_total == 1:
        js.document.active_year = 0
        el.lastChild.remove()
        js.document.plan.years = []
        js.document.getElementById("years_stored_value").innerText = 0
        populate_year_form()
    else:
        js.document.plan.years.pop()
        if el.lastChild.classList.contains("active"):
            el.lastChild.previousSibling.click()
        el.lastChild.remove()


def e_set_years(e):
    years_desired = int(validate_number_input(js.document.getElementById("years_input"), max_=100, min_=1))
    js.document.getElementById("years_input").value = ''
    if not years_desired:
        return None
    el = js.document.getElementById("years_list")
    years_amount = el.childElementCount

    if years_desired > years_amount:
        while years_amount < years_desired:
            trigger_event(e_add_year)
            years_amount = el.childElementCount
    elif years_desired < years_amount:
        while years_amount > years_desired:
            trigger_event(e_remove_year)
            years_amount = el.childElementCount
    else:
        pass


def e_set_monthly_salary(e):
    set_base_param('monthly_salary_stored_value', 'monthly_salary_input', '$', max_=100_000, min_=1)


def e_set_monthly_expenses(e):
    set_base_param('monthly_expenses_stored_value', 'monthly_expenses_input', '$', max_=100_000, min_=0)


def e_set_base_interest_rate(e):
    set_base_param('base_interest_rate_stored_value', 'base_interest_rate_input', '%', max_=100, min_=0)


def e_set_base_inflation_rate(e):
    set_base_param('base_inflation_rate_stored_value', 'base_inflation_rate_input', '%', max_=1000, min_=0)


js.document.getElementById("add_year_btn").onclick = e_add_year
js.document.getElementById("remove_year_btn").onclick = e_remove_year
js.document.getElementById("set_years_btn").onclick = e_set_years
js.document.getElementById("set_monthly_salary_btn").onclick = e_set_monthly_salary
js.document.getElementById("set_monthly_expenses_btn").onclick = e_set_monthly_expenses
js.document.getElementById("set_base_interest_rate_btn").onclick = e_set_base_interest_rate
js.document.getElementById("set_base_inflation_rate_btn").onclick = e_set_base_inflation_rate
js.document.getElementById("prev_year_btn").onclick = e_prev_year_btn
js.document.getElementById("next_year_btn").onclick = e_next_year_btn
