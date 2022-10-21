
# Always import according to index.html - paths: specification, omit everything except the imported file itself
# if  index.html - paths: - src/event_handlers.py
# then you need to "import event_handlers", not "from src import event handlers"

from event_handlers import e_add_year
from helpers import trigger_event
import js

for i in range(12):
    trigger_event(e_add_year)

