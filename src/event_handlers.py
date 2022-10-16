from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event
import js


def e_add_year(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount + 1

    years_count = js.document.getElementById("years_stored_value")
    years_count.textContent = years_total

    li = create_el(type_='li', class_="year-list-item list-group-item sortable-item p-3 col-2")
    el.append(li)

    collapse_btn = create_el('button', class_="btn", custom={"type": "button",
                                                             "data-bs-toggle": "collapse",
                                                             "data-bs-target": f"#collapseExample_{years_total}",
                                                             "aria-expanded": "false",
                                                             "aria-controls": f"collapseExample_{years_total}",
                                                             })
    collapse_body = create_el(class_="collapse", id_=f"collapseExample_{years_total}")

    text1 = create_el(type_='p', class_="text-center", text=f"year {years_total}")
    text2 = create_el(type_='p', class_="text-center", text=f"placeholder")

    # base_interest_rate =
    # base_inflation_rate =
    # max_inflation_rate =
    # max_inflation_rate =

    interest_rate_input = create_el(type_='input', type='range', min=0, max=10, value=5, step=0.01,
                                    oninput="this.nextSibling.value = this.value")
    interest_rate_display = create_el(type_='output', text='0')

    inflation_rate_input = create_el(type_='input', type='range', min=0, max=10, value=5, step=0.01,
                                     oninput="this.nextSibling.value = this.value")
    inflation_rate_display = create_el(type_='output', text='0')

    li.appendChild(collapse_btn)
    li.appendChild(collapse_body)

    collapse_btn.appendChild(text1)
    collapse_body.appendChild(text2)

    collapse_body.appendChild(interest_rate_input)
    collapse_body.appendChild(interest_rate_display)
    collapse_body.appendChild(inflation_rate_input)
    collapse_body.appendChild(inflation_rate_display)


def e_remove_year(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount - 1

    years_count = js.document.getElementById("years_stored_value")
    years_count.value = years_total

    return el.lastChild.remove() if el.lastChild else None


def e_set_years(e):
    years_desired = int(js.document.getElementById("years_input").value)
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
    storage = js.document.getElementById("monthly_salary_stored_value")
    new_val = js.document.getElementById("monthly_salary_input").value
    storage.textContent = new_val


def e_set_living_cost(e):
    storage = js.document.getElementById("living_cost_stored_value")
    new_val = js.document.getElementById("living_cost_input").value
    storage.textContent = new_val


def e_set_base_interest_rate(e):
    storage = js.document.getElementById("base_interest_rate_stored_value")
    new_val = js.document.getElementById("base_interest_rate_input").value
    storage.textContent = new_val


def e_set_base_inflation_rate(e):
    storage = js.document.getElementById("base_inflation_rate_stored_value")
    new_val = js.document.getElementById("base_inflation_rate_input").value
    storage.textContent = new_val


def e_set_max_interest_rate(e):
    storage = js.document.getElementById("max_interest_rate_stored_value")
    new_val = js.document.getElementById("max_interest_rate_input").value
    storage.textContent = new_val


def e_set_max_inflation_rate(e):
    storage = js.document.getElementById("max_inflation_rate_stored_value")
    new_val = js.document.getElementById("max_inflation_rate_input").value
    storage.textContent = new_val


js.document.getElementById("add_year_btn").onclick = e_add_year
js.document.getElementById("remove_year_btn").onclick = e_remove_year
js.document.getElementById("set_years_btn").onclick = e_set_years
js.document.getElementById("set_monthly_salary_btn").onclick = e_set_monthly_salary
js.document.getElementById("set_living_cost_btn").onclick = e_set_living_cost
js.document.getElementById("set_base_interest_rate_btn").onclick = e_set_base_interest_rate
js.document.getElementById("set_max_interest_rate_btn").onclick = e_set_max_interest_rate
js.document.getElementById("set_base_inflation_rate_btn").onclick = e_set_base_inflation_rate
js.document.getElementById("set_max_inflation_rate_btn").onclick = e_set_max_inflation_rate
