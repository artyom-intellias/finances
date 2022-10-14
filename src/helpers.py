import js


def trigger_event(event):
    event(js.document.createEvent('Event'))


def create_el(type_='div', id_=None, class_=None):
    el = js.document.createElement(type_)
    if id_:
        el.setAttribute('id', id_)
    if class_:
        el.setAttribute('class', class_)
    return el

