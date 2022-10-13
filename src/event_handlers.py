from pyodide.ffi import create_proxy
import js


def e_add_year_btn(e):
    el = document.getElementById("years_list")
    years_total = el.childElementCount
    new_li = js.document.createElement("li")
    text = js.document.createTextNode(f"year {years_total}")
    new_li.appendChild(text)
    el.append(new_li)


def e_remove_year_btn(e):
    li = js.document.createElement("li")
    el = document.getElementById("years_list")
    el.lastChild.remove()


def e_set_years_btn(e):
    years_desired = int(document.getElementById("years_input").value)
    el = document.getElementById("years_list")
    years_amount = el.childElementCount
    event = document.createEvent('Event')

    if years_desired > years_amount:
        while years_amount != years_desired:
            e_add_year_btn(event)
            years_amount = el.childElementCount
    elif years_desired < years_amount:
        while years_amount != years_desired:
            e_remove_year_btn(event)
            years_amount = el.childElementCount
    else:
        pass


document.getElementById("add_year_btn").onclick = e_add_year_btn
document.getElementById("remove_year_btn").onclick = e_remove_year_btn
document.getElementById("set_years_btn").onclick = e_set_years_btn
