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


def validate_number_input(el, max_, min_=0, error_timeout=1000):
    val = str(el.value)
    class_toggle = create_proxy(lambda: el.classList.remove('is-invalid'))
    number = to_number(val)
    if number or number == 0:
        if number > max_:
            el.classList.add('is-invalid')
            js.window.setTimeout(class_toggle, error_timeout)
            return ''
        elif number < min_:
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


def set_base_param(storage_id: str, input_id: str, trailing_char: str, min_: int = 0, max_: int = 1):
    storage = js.document.getElementById(storage_id)
    validated_input = validate_number_input(js.document.getElementById(input_id), max_=max_, min_=min_)
    if validated_input:
        storage.textContent = validated_input + f' {trailing_char}'
    js.document.getElementById(input_id).value = ''


def block_base_params(e):
    js.document.getElementById('monthly_salary_input').readOnly = True
    js.document.getElementById('monthly_expenses_input').readOnly = True
    js.document.getElementById('base_interest_rate_input').readOnly = True
    js.document.getElementById('base_inflation_rate_input').readOnly = True


def unblock_base_params(e):
    js.document.getElementById('monthly_salary_input').readOnly = False
    js.document.getElementById('monthly_expenses_input').readOnly = False
    js.document.getElementById('base_interest_rate_input').readOnly = False
    js.document.getElementById('base_inflation_rate_input').readOnly = False


def populate_year_form(year_number=0, year_info=None):
    trim_decimal = lambda val, round_to: float(round(val, round_to))

    def set_info_by_id(id_, key, input=False, round_to=0):
        value = trim_decimal(year_info.report[key], round_to) if year_info else 0
        if input:
            js.document.getElementById(id_).value = value
        else:
            js.document.getElementById(id_).textContent = value

    js.document.getElementById("year_number").textContent = f"Year #{year_number}"

    set_info_by_id('monthly_salary_detailed_input', 'monthly_salary', input=True)
    set_info_by_id('yearly_salary', 'yearly_salary')
    set_info_by_id('monthly_salary_indexed', 'monthly_salary_indexed')
    set_info_by_id('yearly_salary_indexed', 'yearly_salary_indexed')

    set_info_by_id('monthly_expenses_detailed_input', 'monthly_expenses', input=True)
    set_info_by_id('yearly_expenses', 'yearly_expenses')
    set_info_by_id('monthly_expenses_indexed', 'monthly_expenses_indexed')
    set_info_by_id('yearly_expenses_indexed', 'yearly_expenses_indexed')

    set_info_by_id('interest_rate_detailed_input', 'interest_rate', input=True)
    set_info_by_id('yearly_income', 'yearly_income')
    set_info_by_id('yearly_adjusted_income', 'yearly_adjusted_income')
    set_info_by_id('monthly_income', 'monthly_income')
    set_info_by_id('monthly_adjusted_income', 'monthly_adjusted_income')
    set_info_by_id('total_balance', 'total_balance')

    set_info_by_id('inflation_rate_detailed_input', 'inflation_rate', input=True)
    set_info_by_id('monthly_inflated', 'monthly_inflated')
    set_info_by_id('total_inflated', 'total_inflated')
    set_info_by_id('total_adjusted_balance', 'total_adjusted_balance')
    set_info_by_id('yearly_inflated', 'yearly_inflated')

    set_info_by_id('devaluation_rate', 'devaluation_rate', round_to=2)
