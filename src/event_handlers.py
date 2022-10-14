from pyodide.ffi import create_proxy
import js


def e_add_year_btn(e):
    el = js.document.getElementById("years_list")
    years_total = el.childElementCount + 1
    new_li = js.document.createElement("li")
    text = js.document.createTextNode(f"year {years_total}")
    new_li.appendChild(text)
    el.append(new_li)


def e_remove_year_btn(e):
    el = js.document.getElementById("years_list")
    return el.lastChild.remove() if el.lastChild else None


def e_set_years_btn(e):
    years_desired = int(js.document.getElementById("years_input").value)
    el = js.document.getElementById("years_list")
    years_amount = el.childElementCount
    event = js.document.createEvent('Event')

    if years_desired > years_amount:
        while years_amount < years_desired:
            e_add_year_btn(event)
            years_amount = el.childElementCount
    elif years_desired < years_amount:
        while years_amount > years_desired:
            e_remove_year_btn(event)
            years_amount = el.childElementCount
    else:
        pass

def e_set_yearly_inflation(e):...
def e_set_yearly_interest_rate(e):...


js.document.getElementById("add_year_btn").onclick = e_add_year_btn
js.document.getElementById("remove_year_btn").onclick = e_remove_year_btn
js.document.getElementById("set_years_btn").onclick = e_set_years_btn
