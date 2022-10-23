from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event, validate_number_input
import js
from js import localStorage


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
                         class_="btn btn-light col list-group-item sortable-item border year-list-item-btn p-3", custom={"type": "button"})
    btn_text = create_el(type_='span', class_="text-center muted-event-child", text=f"Year #{years_total}")

    year_btn.appendChild(btn_text)
    years_list.appendChild(year_btn)

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

    return el.lastChild.remove() if el.lastChild else None


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


def e_set_living_cost(e):
    storage = js.document.getElementById("living_cost_stored_value")
    validated_input = validate_number_input(js.document.getElementById("living_cost_input"), 100_000)
    if validated_input:
        storage.textContent = validated_input + ' $'
    js.document.getElementById("living_cost_input").value = ''


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


js.document.getElementById("add_year_btn").onclick = e_add_year
js.document.getElementById("remove_year_btn").onclick = e_remove_year
js.document.getElementById("set_years_btn").onclick = e_set_years
js.document.getElementById("set_monthly_salary_btn").onclick = e_set_monthly_salary
js.document.getElementById("set_living_cost_btn").onclick = e_set_living_cost
js.document.getElementById("set_base_interest_rate_btn").onclick = e_set_base_interest_rate
js.document.getElementById("set_base_inflation_rate_btn").onclick = e_set_base_inflation_rate
js.document.getElementById("prev_year_btn").onclick = e_prev_year_btn
js.document.getElementById("next_year_btn").onclick = e_next_year_btn
