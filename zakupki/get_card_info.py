from selenium_setup import get_driver
from database import Data_base_API
from product_cadr_reader import *
from convert import string_to_int, string_to_datetime

import time


def parse_table(driver, contract_id):
    # ПАРСИНГ ТАБЛИЦЫ
    row_xpath = '//*[@id="contractSubjects"]/div/div/div/div[1]/table/tbody/tr[@class="tableBlock__row "]'
    rows = driver.find_elements_by_xpath(row_xpath)
    products = []

    counter = 0
    for row in rows:
        product_info = {}
        relative_cell_xpath = './/td'
        cells = row.find_elements_by_xpath(relative_cell_xpath)
        product_info = product_info | get_product_name_country(cells[1].text)
        product_info = product_info | get_ktru_okpd_2(product_info, cells[2].text)
        product_info = product_info | get_product_type(cells[3].text)
        product_info = product_info | get_quantity_measure(cells[4].text)
        product_info = product_info | get_price(cells[5].text)
        product_info = product_info | get_cost_tax(cells[7].text)
        product_info['contrant_card_id'] = contract_id
        # print(product_info)
        products.append(product_info)
        counter +=1
    DB_API.products.insert_list(products)

    # print(f'Добавлено {counter} товаров в {contract_id}')
    # return products
    return None

def read_product_page(driver, contract_id):
    product_table_xpath = '//table[@class="blockInfo__table tableBlock grayBorderBottom"]'
    table = driver.find_element_by_xpath(product_table_xpath)
    time.sleep(0.5)
    # КОЛИЧЕСВТО ТОВАРОВ
    product_amount_xpath = './/span[@class="tableBlock__resultTitle"]'
    product_amount = string_to_int(table.find_element_by_xpath(product_amount_xpath).text)
    # print(product_amount)
    if product_amount <= 10:
        # print(f"Не больше 10 товаров на странице ({product_amount})")
        # ПРОСТО ПАРСИМ
        products = parse_table(driver, contract_id)

    elif product_amount <= 50:
        # print(f"Не больше 50 товаров на странице ({product_amount})")
        # ЖМЕМ КНОПКУ "ПОКАЗАТЬ ПО: 50" И ПАРСИМ
        driver.find_element_by_xpath('//*[@id="contractSubjects"]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/span').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="_50"]').click()
        time.sleep(0.5)

        products = parse_table(driver, contract_id)

    else:
        # print(f"больше 50 товаров на странице ({product_amount})")
        # ЖМЕМ КНОПКУ ПОКАЗАТЬ ПО: 50" ПАРСИМ И ЛИСТАЕМ СТРАНИЦЫ
        driver.find_element_by_xpath('//*[@id="contractSubjects"]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/span').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="_50"]').click()
        time.sleep(0.5)

        condition = True

        while condition:
            products = parse_table(driver, contract_id)

            navigation_ul = driver.find_elements_by_xpath('//*[@id="contractSubjectSearchPositionNavigation"]/ul/li')
            last_arrow = navigation_ul[-1]

            if 'disabled' in last_arrow.get_attribute('class'):
                # print('End')
                condition = False
            else:
                # print('Continue')
                last_arrow.click()
                time.sleep(0.5)




from database.tables import Contrant_card, Product
from sqlalchemy import select

# отбор контрактов, которые не парсились
from_date = string_to_datetime('31/12/2022')

DB_API = Data_base_API()
stmt = select(Contrant_card.number).where(Contrant_card.date > from_date)
stmt2 = select(Product.contrant_card_id)
contracts = set(DB_API.contrant_cards.session.execute(stmt).all())
products = set(DB_API.contrant_cards.session.execute(stmt2).all())

contract_to_parse = contracts - products
contract_amount = len(contract_to_parse)

print(contract_amount)
start_page = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='

DRIVER = get_driver()

contract_counter = 0
error_counter = 1
for contract_tuple in contract_to_parse:
    contract = DB_API.contrant_cards.select(number = contract_tuple[0])
    reestr_number = str(contract.number)
    product_page = f'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber={reestr_number}'

    if not contract.products:
        DRIVER.get(product_page)
        card_info_xpath = '//span[@class="cardMainInfo__content"]'

        update_date = DRIVER.find_elements_by_xpath(card_info_xpath)[-1]

        # print(update_date.text)
        # contract.update_date = string_to_datetime(update_date.text)
        # DB_API.contrant_cards.save(contract)
        # print(contract)
        try:
            read_product_page(DRIVER, contract.number)
        except:
            error_counter += 1
        contract_counter += 1
    else:
        contract_counter += 1
    print(f'Всего: {contract_amount}, готово: {contract_counter}, ошибки: {error_counter}', end = '\r')

DRIVER.quit()
