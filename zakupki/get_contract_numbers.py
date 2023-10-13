from settings import START_DATE, END_DATE, DAYS_STEP#, DATA_BASE_PATH

from date_setup import get_days
from selenium_setup import get_driver
import time
from convert import string_to_int, string_to_float, string_to_datetime
from database import Data_base_API

def setup_site_filter(DRIVER):
    # Настройка параметров поиска
        # Клики по "квадратикам"
        # завершенные контракты + Настройка на количество страниц 50 шт.
    param_list = ['//*[@id="contractStageListTag"]/div/div[2]/div[4]/label',
                    '//*[@id="contractStageListTag"]/div/div[2]/div[1]/label',
                    '//*[@id="contractStageListTag"]/div/div[2]/div[3]/label',
                    '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/span',
                    '//*[@id="_50"]']

    [DRIVER.find_element_by_xpath(el).click() for el in param_list]

        # Выбор Города
    citi_chose = '//*[@id="customerPlaceAnchor"]'
    DRIVER.find_element_by_xpath(citi_chose).click()
    print('Два *')
    citi_input = '//*[@id="goodssearch"]'
    DRIVER.find_element_by_xpath(citi_input).send_keys('Санкт-Петербург')
    aply_btn = '//*[@id="btn-floating"]/button'
    print('вставили спб *')
    time.sleep(1) # Нужно подождать пока найдет СПБ
    spb_cell = '//*[@id="mCSB_2_container"]/ul/li[1]/span'
    DRIVER.find_element_by_xpath(spb_cell).click()
    print('кликнули спб *')
    aply_btn = '//*[@id="modal-okdp-okved"]/div/div[4]/div/div/button[2]'
    DRIVER.find_element_by_xpath(aply_btn).click()
    print('Применили')

def clear_dateform(DRIVER):
    # очистка формы даты (нажать на кнопу "до" и пустую часть)
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    DRIVER.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[2]'
    DRIVER.find_element_by_xpath(date_set_to).click()
    DRIVER.find_element_by_xpath("//html").click()

def clear_dateform2(DRIVER):
    # очистка формы даты (нажать на кнопу "от" и пустую часть)
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    DRIVER.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[1]'
    DRIVER.find_element_by_xpath(date_set_to).click()
    DRIVER.find_element_by_xpath("//html").click()

def date_input(DRIVER, d_from, d_to):
    # Выбор даты
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    DRIVER.find_element_by_xpath(date_form).click()
    DRIVER.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[2]'
    DRIVER.find_element_by_xpath(date_set_to).click()
    date_from = '//*[@id="contractDateTag"]/div/div/div/div[1]/input'
    DRIVER.find_element_by_xpath(date_from).send_keys(d_from)
    date_to = '//*[@id="contractDateTag"]/div/div/div/div[2]/input'
    DRIVER.find_element_by_xpath(date_to).send_keys(d_to)
    DRIVER.find_element_by_xpath(date_form).click()
    DRIVER.find_element_by_xpath("//html").click()
    aply_btn = '//*[@id="btn-floating"]/button'
    DRIVER.find_element_by_xpath(aply_btn).click()

def read_amount(DRIVER):
    # Смотрим, сколько вариантов нашлось
    found_list = []
    result = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[1]/div[2]'
    result = DRIVER.find_element_by_xpath(result)
    found_list = [el for el in result.text if el in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}]
    #print(int("".join(found_list)))
    if found_list:
        return int("".join(found_list))
    else:
        return 0

def read_page(DRIVER):
    contrant_cards = []
    # считываем все номера со страницы

    contrant_card_xpath = '//div[@class="row no-gutters registry-entry__form mr-0"]'
    contrant_card_elements = DRIVER.find_elements_by_xpath(contrant_card_xpath)

    for c_c_elem in contrant_card_elements:
        try:
            contrant_cards.append(
                {
                'number': string_to_int(c_c_elem.find_element_by_xpath('.//div[@class="registry-entry__header-mid__number"]').text),
                'date': string_to_datetime(c_c_elem.find_element_by_xpath('.//div[@class="data-block__value"]').text),
                'price': string_to_float(c_c_elem.find_element_by_xpath('.//div[@class="price-block__value"]').text),
                'customer': c_c_elem.find_element_by_xpath('.//div[@class="registry-entry__body-href"]').text,
                }
            )
        except:
            continue

    return contrant_cards

def parse_numbers():
    # открываем сайт
    DRIVER = get_driver()
    DB_API = Data_base_API()#DATA_BASE_PATH)
    # настраиваем фильтры
    setup_site_filter(DRIVER)

    days_list = get_days(START_DATE, END_DATE)

    step = DAYS_STEP
    day_index = 0
    period = 0
    sum_kontrakts = 0
    error_date = []

    while day_index < len(days_list):
        pre_index = day_index # что бы переписать даты
        day_from = days_list[day_index]
        day_index += step
        if day_index >= len(days_list):
            day_index = len(days_list) - 1
        day_to =  days_list[day_index]
        day_index += 1
        period = day_index - pre_index
        # вставляем даты в поисковик
        date_input(DRIVER, day_from, day_to)
        some_text = read_amount(DRIVER)
        print(f'от: {day_from} до: {day_to}, контрактов: {some_text}')
        # Проверяем, что бы значений было меньше 999
        if some_text > 999 and period > 1:
            day_index = pre_index
            step -= 1
            clear_dateform(DRIVER)
        else:
            if period < 2 and some_text > 999:
                # error_date.append([day_from, day_to])
                print('--- Период = 1, контрактов больше 999!!')
            ## Начинаем цикл с перелистыванием и парсингом
            pars_pages_stat = 0
            page_number = 0

            print(f'Кол-во контрактов: {some_text}')
            while pars_pages_stat == 0:
                # парсим карточки контрактов со страницы

                contrant_cards = read_page(DRIVER)
                for el in contrant_cards:
                    # print(el)
                    DB_API.contrant_cards.insert(**el)

                # Перелистывание страницы
                xp_pg_nums = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[1]/ul/a'
                pg_num = DRIVER.find_elements_by_xpath(xp_pg_nums)
                # ловим стрелку перемотки
                if page_number != 0:
                    # если это не первая страница - в списке две стрелки
                    if len(pg_num) == 2:
                        pg_num[1].click()
                        page_number += 1
                    else:
                    # в списке одна стрелка и стр. не №1 = последняя стр.
                        print('Закончили перелистывать')

                        pars_pages_stat = 1
                else:
                    # если это первая страница - в списке одна стрелка - сслыка
                    pg_num[0].click()
                    page_number += 1

            print(f'Скачали: {some_text} шт. за период {period} дн.')
            sum_kontrakts += some_text
            print(f'Всего скачано: {sum_kontrakts} шт.')
            step = DAYS_STEP
            if period == 1:
                clear_dateform2(DRIVER)
            else:
                clear_dateform(DRIVER)
