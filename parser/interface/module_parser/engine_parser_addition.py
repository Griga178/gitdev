import re
from datetime import date

def clean_number(str_text):
    ''' Выводит только числа из строк с помощью регулярок
        находит числа, в которых "." или "," используется
        только для копеек'''
    result = re.findall(r'\d+\.?\,?', str_text)

    clear_number = ''.join(result)

    if ',' in clear_number:
        clear_number = clear_number.replace(',', '.')
    try:
        clear_number = float(clear_number)
        return clear_number
    except:
        clear_number = f"!Не преобразовать в число:{str_text}"
        return clear_number

def clean_text(str_text):
    str_text = " ".join(str_text.split())
    return str_text

def set_current_date():
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")

    return current_date

def set_true(usless_t = False):
    # ЕСЛИ НАХОДИТ ЭТОТ ТЕГ, ЗНАЧИТ ТОВАРА НЕТ В НАЛИЧИИ
    return True
