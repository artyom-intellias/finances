import js
from pyodide.ffi import create_proxy

def trigger_event(event):
    event(js.document.createEvent('Event'))


def create_el(type_='div', id_=None, class_=None, text='', **kwargs):
    el = js.document.createElement(type_)
    if id_:
        el.setAttribute('id', id_)
    if class_:
        el.setAttribute('class', class_)
    if text:
        el.innerHTML = text
    for k, v in kwargs.items():
        if isinstance(v, dict):
            for k_k, k_v in v.items():
                el.setAttribute(k_k, k_v)
            continue
        el.setAttribute(k, v)

    return el


def validate_input(el, max, min=0, error_timeout=1000):
    val = el.value
    class_toggle = create_proxy(lambda: el.classList.remove('is-invalid'))
    if val.isdigit():
        if int(val) > max:
            el.classList.add('is-invalid')
            js.window.setTimeout(class_toggle, error_timeout)
            return ''
        elif int(val) < min:
            el.classList.add('is-invalid')
            js.window.setTimeout(class_toggle, error_timeout)
            return ''
        else:
            el.classList.remove("is-invalid")
            js.window.setTimeout(class_toggle, error_timeout)
            return str(val)
    elif val == '':
        return ''
    else:
        el.classList.add('is-invalid')
        js.window.setTimeout(class_toggle, error_timeout)
        return ''
