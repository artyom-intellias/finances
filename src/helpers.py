import js


def trigger_event(event):
    event(js.document.createEvent('Event'))
