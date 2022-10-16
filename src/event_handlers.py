from pyodide.ffi import create_proxy
from helpers import create_el, trigger_event
import js


def e_add_year_btn(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount + 1

    years_total_span = js.document.getElementById("years_count")
    years_total_span.textContent = years_total

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
    interest_rate_input = create_el(type_='input',
                                    class_=f"interest_rate_input_{years_total} form-control bg-success text-white")
    inflation_input = create_el(type_='input',
                                class_=f"inflation_input_{years_total} form-control bg-danger text-white")

    li.appendChild(collapse_btn)
    li.appendChild(collapse_body)

    collapse_btn.appendChild(text1)
    collapse_body.appendChild(text2)

    collapse_body.appendChild(interest_rate_input)
    collapse_body.appendChild(inflation_input)


def e_remove_year_btn(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount - 1

    years_total_span = js.document.getElementById("years_count")
    years_total_span.textContent = years_total

    return el.lastChild.remove() if el.lastChild else None


def e_set_years_btn(e):
    years_desired = int(js.document.getElementById("years_input").value)
    el = js.document.getElementById("years_list")
    years_amount = el.childElementCount

    if years_desired > years_amount:
        while years_amount < years_desired:
            trigger_event(e_add_year_btn)
            years_amount = el.childElementCount
    elif years_desired < years_amount:
        while years_amount > years_desired:
            trigger_event(e_remove_year_btn)
            years_amount = el.childElementCount
    else:
        pass


def e_set_yearly_inflation(e): ...


def e_set_yearly_interest_rate(e): ...


js.document.getElementById("add_year_btn").onclick = e_add_year_btn
js.document.getElementById("remove_year_btn").onclick = e_remove_year_btn
js.document.getElementById("set_years_btn").onclick = e_set_years_btn
