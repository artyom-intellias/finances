
# Always import according to - paths: specification, omit actual path, and point to exact file
from event_handlers import e_add_year_btn

for i in range(10):
    event = document.createEvent('Event')
    e_add_year_btn(event)
