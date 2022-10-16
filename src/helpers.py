import js


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


def validate_input(el, max, min=0):
    val = el.value
    if val.isdigit():
        if int(val) > max:
            el.classList.add('is-invalid')
            return ''
        elif int(val) < min:
            el.classList.add('is-invalid')
            return ''
        else:
            el.classList.remove("is-invalid")
            return str(val)
    elif val == '':
        return ''
    else:
        el.classList.add('is-invalid')
        return ''
