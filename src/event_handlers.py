from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event, validate_number_input
from plan_composer import PlanComposer
import js


def populate_year_form(year_number, year_info):
    print(year_info)

    squize = lambda x: float(round(x, 1))

    js.document.getElementById("year_number").textContent = f"Year #{year_number}"

    js.document.getElementById("monthly_salary_detailed_input").value = squize(year_info.report['monthly_salary'])
    js.document.getElementById("yearly_salary").textContent = squize(year_info.report['yearly_salary'])
    js.document.getElementById("monthly_salary_indexed").textContent = squize(year_info.report['monthly_salary_indexed'])
    js.document.getElementById("yearly_salary_indexed").textContent = squize(year_info.report['yearly_salary_indexed'])

    js.document.getElementById("monthly_expenses_detailed_input").value = squize(year_info.report['monthly_expenses'])
    js.document.getElementById("yearly_expenses").textContent = squize(year_info.report['yearly_expenses'])
    js.document.getElementById("monthly_expenses_indexed").textContent = squize(year_info.report['monthly_expenses_indexed'])
    js.document.getElementById("yearly_expenses_indexed").textContent = squize(year_info.report['yearly_expenses_indexed'])

    js.document.getElementById("interest_rate_detailed_input").value = squize(year_info.interest_rate)
    js.document.getElementById("yearly_income").textContent = squize(year_info.report['yearly_income'])
    js.document.getElementById("yearly_adjusted_income").textContent = squize(year_info.report['yearly_adjusted_income'])
    js.document.getElementById("monthly_income").textContent = squize(year_info.report['monthly_income'])
    js.document.getElementById("monthly_adjusted_income").textContent = squize(year_info.report['monthly_adjusted_income'])
    js.document.getElementById("total_income").textContent = squize(year_info.report['total_income'])
    js.document.getElementById("total_adjusted_income").textContent = squize(year_info.report['total_adjusted_income'])

    js.document.getElementById("inflation_rate_detailed_input").value = squize(year_info.inflation_rate)
    js.document.getElementById("monthly_inflated").textContent = squize(year_info.report['monthly_inflated'])
    js.document.getElementById("yearly_inflated").textContent = squize(year_info.report['yearly_inflated'])
    js.document.getElementById("total_inflated").textContent = squize(year_info.report['total_inflated'])
    # print(year_info.report['total_inflated'])


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
    storage = js.document.getElementById("monthly_salary_stored_value")
    validated_input = validate_number_input(js.document.getElementById("monthly_salary_input"), 100_000, min=1)
    if validated_input:
        storage.textContent = validated_input + ' $'
    js.document.getElementById("monthly_salary_input").value = ''


def e_set_monthly_expenses(e):
    storage = js.document.getElementById("monthly_expenses_stored_value")
    validated_input = validate_number_input(js.document.getElementById("monthly_expenses_input"), 100_000)
    if validated_input:
        storage.textContent = validated_input + ' $'
    js.document.getElementById("monthly_expenses_input").value = ''


def e_set_base_interest_rate(e):
    storage = js.document.getElementById("base_interest_rate_stored_value")
    validated_input = validate_number_input(js.document.getElementById("base_interest_rate_input"), 100)
    if validated_input:
        storage.textContent = validated_input + ' %'
    js.document.getElementById("base_interest_rate_input").value = ''


def e_set_base_inflation_rate(e):
    storage = js.document.getElementById("base_inflation_rate_stored_value")
    validated_input = validate_number_input(js.document.getElementById("base_inflation_rate_input"), 1000)
    if validated_input:
        storage.textContent = validated_input + ' %'
    js.document.getElementById("base_inflation_rate_input").value = ''


def e_generate_plan(e):
    monthly_salary = float(js.document.getElementById("monthly_salary_stored_value").innerText[:-2])
    monthly_expenses = float(js.document.getElementById("monthly_expenses_stored_value").innerText[:-2])
    interest_rate = float(js.document.getElementById("base_interest_rate_stored_value").innerText[:-2])
    inflation_rate = float(js.document.getElementById("base_inflation_rate_stored_value").innerText[:-2])
    years_total = int(js.document.getElementById("years_stored_value").innerText)
    js.document.plan = PlanComposer(monthly_salary=monthly_salary, monthly_expenses=monthly_expenses,
                                    interest_rate=interest_rate,
                                    inflation_rate=inflation_rate, years_total=years_total)


js.document.getElementById("add_year_btn").onclick = e_add_year
js.document.getElementById("remove_year_btn").onclick = e_remove_year
js.document.getElementById("set_years_btn").onclick = e_set_years
js.document.getElementById("set_monthly_salary_btn").onclick = e_set_monthly_salary
js.document.getElementById("set_monthly_expenses_btn").onclick = e_set_monthly_expenses
js.document.getElementById("set_base_interest_rate_btn").onclick = e_set_base_interest_rate
js.document.getElementById("set_base_inflation_rate_btn").onclick = e_set_base_inflation_rate
js.document.getElementById("prev_year_btn").onclick = e_prev_year_btn
js.document.getElementById("next_year_btn").onclick = e_next_year_btn
js.document.getElementById("generate_investment_plan_btn").onclick = e_generate_plan
