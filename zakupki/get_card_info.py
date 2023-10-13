from selenium_setup import get_driver
from convert import string_to_int, string_to_float, string_to_datetime, clean_string
from database import Data_base_API

DB_API = Data_base_API()


c = DB_API.contrant_cards.select(number = 1372903073923000003)
print(c)
# print(len(c))
start_page = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='



DRIVER = get_driver()


reestr_number = str(c.number)
product_page = f'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber={reestr_number}'

DRIVER.get(product_page)

def product_name_country(cell):
    # '3. Источник вторичного электропитания резервированный Smartec ST-PS103\nСтрана происхождения: КИТАЙ (156)'
    info = cell.split('\n')
    values = {}
    values['name'] = info[0][3:]
    values['country_producer'] = info[1].replace('Страна происхождения: ', '') if 'Страна' in info[1] else None

    # print(values)
    return values

def read_product_page(driver):
    products = []



    row_xpath = '//*[@id="contractSubjects"]/div/div/div/div[1]/table/tbody/tr[@class="tableBlock__row "]'
    rows = driver.find_elements_by_xpath(row_xpath)
    for row in rows:
        relativ_cell_xpath = './/td'
        cells = row.find_elements_by_xpath(relativ_cell_xpath)
        print(product_name_country(cells[1].text))
        # for cell in cells:
        #     print(clean_string(cell.text))

read_product_page(DRIVER)



# ktru = Column(Text)
# okpd_2 = Column(Text)
# measure = Column(Text)
# quantity = Column(Float)
# price = Column(Float)
# cost = Column(Float)
# tax = Column(Text)
