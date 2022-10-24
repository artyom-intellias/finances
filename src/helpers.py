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


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def to_number(val: str) -> int or float or None:
    if ',' in val or '.' in val:
        val = val.replace(',', '.')
        if isfloat(val):
            return float(val)
        else:
            return None
    else:
        if val.isdigit():
            return int(val)
        else:
            return None


def validate_number_input(el, max, min=0, error_timeout=1000):
    val = str(el.value)
    class_toggle = create_proxy(lambda: el.classList.remove('is-invalid'))
    number = to_number(val)
    if number:
        if number > max:
            el.classList.add('is-invalid')
            js.window.setTimeout(class_toggle, error_timeout)
            return ''
        elif number < min:
            el.classList.add('is-invalid')
            js.window.setTimeout(class_toggle, error_timeout)
            return ''
        else:
            el.classList.remove("is-invalid")
            js.window.setTimeout(class_toggle, error_timeout)
            return str(number)
    elif val == '':
        return ''
    else:
        el.classList.add('is-invalid')
        js.window.setTimeout(class_toggle, error_timeout)
        return ''


def set_base_param(storage_id: str, input_id: str, trailing_char: str, min: int = 0, max: int = 1):
    storage = js.document.getElementById(storage_id)
    validated_input = validate_number_input(js.document.getElementById(input_id), max=max, min=min)
    if validated_input:
        storage.textContent = validated_input + f' {trailing_char}'
    js.document.getElementById(input_id).value = ''
