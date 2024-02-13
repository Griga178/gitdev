from requests import Response
from bs4 import BeautifulSoup
from convert_data import *
import re

def get_contract_amount(response: Response):
    '''    Количество найденных котрактов    '''
    soup = BeautifulSoup(response.text, 'html.parser')
    amount_div = soup.find("div", {"class": "search-results__total"})
    contract_amount_numbers = re.findall(r'\d', amount_div.string)
    if contract_amount_numbers:
        contract_amount = int(''.join(contract_amount_numbers))
    else:
        contract_amount = 0
    return contract_amount

def get_page_amount(contract_amount, c_per_page = 50):
    page_amount = contract_amount // c_per_page + 1
    return page_amount

def get_contract_numbers(response: Response):
    '''    Парсим номера и выводимую инфу со страницы    '''
    contrant_cards = []

    soup = BeautifulSoup(response.text, 'html.parser')
    cntr_divs = soup.find_all("div", {"class": "row no-gutters registry-entry__form mr-0"})

    q_co = 0

    for cntr_block in cntr_divs:
        q_co += 1
        dates = cntr_block.find_all("div", {"class": "data-block__value"})

        c_c = {
        'number': string_to_int(cntr_block.find("div", {"class": "registry-entry__header-mid__number"}).a.string),
        'date': string_to_datetime(dates[0].string),
        'execute_date': string_to_datetime(dates[1].string),
        'place_date': string_to_datetime(dates[2].string),
        'update_date': string_to_datetime(dates[3].string),
        'price': string_to_float(cntr_block.find("div", {"class": "price-block__value"}).string),
        'customer': clean_string(cntr_block.find("div", {"class": "registry-entry__body-href"}).a.string)
        }
        contrant_cards.append(c_c)
        # print(q_co, c_c)
    return contrant_cards
