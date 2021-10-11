'''парсинг еис
Контракты:
Санкт-Петербург {'178', '278', '378'}
Ленинградская обл.
2021 год
2020 год
'Исполнение завершено'
'''
import time
from selenium import webdriver
import pickle

page = 'https://zakupki.gov.ru/epz/contract/search/results.html'


driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

driver.get(page)

def first_setting():
    # Настройка параметров поиска
        # Клики по "квадратикам"
        # Настройка на количество страниц 50 шт.
    param_list = ['//*[@id="contractStageListTag"]/div/div[2]/div[4]/label',
                    '//*[@id="contractStageListTag"]/div/div[2]/div[1]/label',
                    '//*[@id="contractStageListTag"]/div/div[2]/div[3]/label',
                    '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/span',
                    '//*[@id="_50"]']

    [driver.find_element_by_xpath(el).click() for el in param_list]


        # Выбор Города
    citi_chose = '//*[@id="customerPlaceAnchor"]'
    driver.find_element_by_xpath(citi_chose).click()
    print('Два *')
    citi_input = '//*[@id="goodssearch"]'
    driver.find_element_by_xpath(citi_input).send_keys('Санкт-Петербург')
    aply_btn = '//*[@id="btn-floating"]/button'
    print('вставили спб *')
    time.sleep(1) # Нужно подождать пока найдет СПБ
    spb_cell = '//*[@id="mCSB_2_container"]/ul/li[2]/span'
    driver.find_element_by_xpath(spb_cell).click()
    print('кликнули спб *')
    aply_btn = '//*[@id="modal-okdp-okved"]/div/div[4]/div/div/button[2]'
    driver.find_element_by_xpath(aply_btn).click()
    print('Применили')

def clear_dateform():
    # очистка формы даты (нажать на кнопу "до" и пустую часть)
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    driver.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[2]'
    driver.find_element_by_xpath(date_set_to).click()
    driver.find_element_by_xpath("//html").click()

def clear_dateform2():
    # очистка формы даты (нажать на кнопу "от" и пустую часть)
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    driver.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[1]'
    driver.find_element_by_xpath(date_set_to).click()
    driver.find_element_by_xpath("//html").click()

def date_input(d_from, d_to):
    # Выбор даты
    date_form = '//*[@id="contractDateTag"]/div/div/div'
    driver.find_element_by_xpath(date_form).click()
    driver.find_element_by_xpath(date_form).click()
    date_set_to = '//*[@id="calendarDays"]/div[1]/button[2]'
    driver.find_element_by_xpath(date_set_to).click()
    date_from = '//*[@id="contractDateTag"]/div/div/div/div[1]/input'
    driver.find_element_by_xpath(date_from).send_keys(d_from)
    date_to = '//*[@id="contractDateTag"]/div/div/div/div[2]/input'
    driver.find_element_by_xpath(date_to).send_keys(d_to)
    driver.find_element_by_xpath(date_form).click()
    driver.find_element_by_xpath("//html").click()
    aply_btn = '//*[@id="btn-floating"]/button'
    driver.find_element_by_xpath(aply_btn).click()

def read_amount():
    # Смотрим, сколько вариантов нашлось
    found_list = []
    result = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[1]/div[2]'
    result = driver.find_element_by_xpath(result)
    found_list = [el for el in result.text if el in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}]
    #print(int("".join(found_list)))
    return int("".join(found_list))

def page_data_save(file_name):
    # Чтение и запись номеров контрактов
        # считываем все номера со страницы
    cells = '//div[@class="registry-entry__header-mid__number"]'
    numbers = driver.find_elements_by_xpath(cells)
        # записываем все "чистые" номера во множество
    numersss = set()
    for el in numbers:
        split_el = str(el.text.split(" ")[1])
        numersss.add(split_el)
        # Пытаемся открыть файл .pkl если есть
    pickle_set = {}
    try:
        with open(file_name, 'rb') as f:
            pickle_set = pickle.load(f)
            numersss |= pickle_set
    except:
        print('no file')

        # добавляем в файл pkl
    with open(file_name, 'wb') as f:
        pickle.dump(numersss, f, pickle.HIGHEST_PROTOCOL)
        print(f'Всего в файле: {len(numersss)} номеров')
    #print(numersss)

###
### Рабочая часть
###
# Формируем список из дат (365 дней) = days_list
max_days_list = [31, 27, 31, 30, 31, 30, 31, 31, 30] # до сент., 31, 30, 31 # 
# на сайте нет 28 февраля!!
mounth_count = 2
year_str = '2021'
days_list = []
for month in max_days_list:
    # добавляем '0' к месяцу
    if len(str(mounth_count)) >= 2:
        monthe = str(mounth_count)
    else:
        monthe = '0' + str(mounth_count)
    mounth_count += 1
    for day in range(month):
        # добавляем '0' к дню
        if len(str(day + 1)) >= 2:
            day_str = str(day + 1)
        else:
            day_str = '0' + str(day + 1)
        days_list.append(f'{day_str}.{monthe}.{year_str}')


first_setting()
#a = input('Проверьте настройки и введите, что нибудь для продолжения')

# Выводит нужные даты если не подходит, то "до" уменьшается на 1 день
first_value = 5 # стандартная разница между датами (от 01 до 05)
step = first_value
day_index = 101 #  начинаем с **.**.2021
period = 0
error_date = []

sum_kontrakts = 0
pkl_name_part = 9

# перебор всех дат
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
    date_input(day_from, day_to)
    some_text = read_amount()
    print(f'от: {day_from} до: {day_to}, контрактов: {some_text}')
    # Проверяем, что бы значений было меньше
    if some_text > 999 and period > 1:
        day_index = pre_index
        step -= 1
        clear_dateform()
    else:
        if period < 2 and some_text > 999:
            error_date.append([day_from, day_to])
            print('--- Период = 1, контрактов больше 999!!')
        ## Начинаем цикл с перелистыванием и парсингом
        pars_pages_stat = 0
        page_number = 0
        print(f'Записываем в файл № {pkl_name_part}')
        print(f'Кол-во контрактов: {some_text}')
        while pars_pages_stat == 0:
            # Перелистывание страницы
            page_data_save('contra/pkl_' + str(pkl_name_part) + '.pkl')
            xp_pg_nums = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[1]/ul/a'
            pg_num = driver.find_elements_by_xpath(xp_pg_nums)
            # ловим стрелку перемотки
            if page_number != 0:
                # если это не первая страница - в списке две стрелки
                if len(pg_num) == 2:
                    pg_num[1].click()
                    page_number += 1
                else:
                # в списке одна стрелка и стр. не №1 = последняя стр.
                    print('Закончили перелистывать')
                    pkl_name_part += 1
                    pars_pages_stat = 1
            else:
                # если это первая страница - в списке одна стрелка - сслыка
                pg_num[0].click()
                page_number += 1
            #

        print(f'Скачали: {some_text} шт. за период {period} дн.')
        sum_kontrakts += some_text
        print(f'Всего скачано: {sum_kontrakts} шт.')
        step = first_value
        if period == 1:
            clear_dateform2()
        else:
            clear_dateform()

        ##
    #pkl_name_part += 1



print(error_date)
