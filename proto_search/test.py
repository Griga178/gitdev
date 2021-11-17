import sys
import time
import pickle
from selenium import webdriver
from lxml import etree, html

page = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber=2781930090921000019&contractInfoId=66596577'
#page = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber=2780610397421000011&contractInfoId=64745227'

driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?
driver.get(page)

#goods_link = '/html/body/div[2]/div/div[1]/div[3]/div/a[2]'
#driver.find_element_by_xpath(goods_link).click()

#full_page_path = '//*[@id="contractSubjects"]/div/div'



def clear_cell(dirty_td):
    content = dirty_td.text_content().strip()
    if '\n' in content:
        content = ' '.join(content.replace('\n', '').split())
    if "\xa0" in content:
        content = content.replace('\xa0', '')
    return content

def string_to_float(value):
    float_number = []
    reg_numb = ''
    for el in value:
        if el in {'1', '2', '3', '4', '5', '6', '7', '8','9', '0', ',', '.'}:
            float_number.append(el)
    if float_number:
        reg_numb = (''.join(float_number)).replace(',', '.')
        return float(reg_numb)
    else:
        return value

def okpd_ktru_values(content):
    # разделение ячейки ОКПД КТРУ на 2 кода
    first_list = content.split(')')
    if len(first_list) == 3:
        # если в ячейке два кода
        first_string = first_list[0].split('(')
        second_string = first_list[1].split('(')
        first_code = first_string[1].strip()
        second_code = second_string[1].strip()
        content = [first_code, second_code]
    elif len(first_list) == 2:
        first_string = first_list[0].split('(')
        first_code = first_string[1].strip()
        content = [first_code]
    code_dict = {}
    for code in content:
        if '-' in code:
            code_dict = code_dict | {'КТРУ': code}
        else:
            code_dict = code_dict | {'ОКПД2': code}
    return code_dict

def table_pars_two():
    # Создаем список наименований с вложенными словарями
    list_name_char = []
    # адрес таблицы
    full_page_path = '//*[@id="contractSubjects"]/div/div/div/div[1]/table/tbody'
    table_pars_code = driver.find_element_by_xpath(full_page_path).get_attribute("outerHTML")
    # все строки таблицы
    rows = html.fromstring(table_pars_code).xpath('//tr/td')
    # Создаем словарь Наименование - Характеристика
    char_value = {}

    count = 0
    for cell in rows:
        count += 1

        if count == 1:
            pass
        elif count == 2:
            name_of_good = clear_cell(cell)
            if 'Страна происхождения' in name_of_good:
                value_list = name_of_good.split('Страна происхождения')
                goods_name = value_list[0].strip()
                country = value_list[1].replace(':', '').strip()
                code_dict = {'Страна происхождения': country}
                char_value = char_value | code_dict
                #print(goods_name)
                #print(code_dict)
            else:
                print("Наименование:", name_of_good)
        elif count == 3:
            # добавляем в словарь коды ОКПД2 и КТРУ если есть
            content = clear_cell(cell)
            dict_content = okpd_ktru_values(content)
            code_of_good = content.split(')')
            #print(dict_content)
            char_value = char_value | dict_content
        elif count == 4:
            # Добавляем тип Объекта
            content = clear_cell(cell)
            char_value = char_value | {'Тип объекта': content}
            #print({'Тип объекта': content})
        elif count == 5:
            # Добавляем количество и ед изм
            content = clear_cell(cell)
            content = content.split()
            if len(content) == 2:
                measure = content[-1]
                amount = string_to_float(content[0])
                cont_dict = {"Количество": amount, "ЕД. ИЗМ.": measure}
            else:
                cont_dict = {"Количество, ЕД. ИЗМ.": ' '.join(content)}
            #print(cont_dict)
            char_value = char_value | cont_dict
        elif count == 6:
            # Добавляем Цена за единицу
            content = clear_cell(cell)
            cont_dict = {"Цена за единицу": string_to_float(content)}
            char_value = char_value | cont_dict
            #print(cont_dict)
        elif count == 7:
            # Добавляем сумму и ставку НДС
            content = clear_cell(cell)
            content = content.split("Ставка НДС:")
            value_nds = content[-1].strip()
            value_sum = string_to_float(content[0])
            cont_dict = {"Сумма": value_sum, "Ставка НДС": value_nds}
            char_value = char_value | cont_dict
            #print(cont_dict)

        elif count == 8:
            # пустая ячейка
            pass

        elif count == 9:
            #if len(cell):
            content = clear_cell(cell)
            if 'Страна происхождения' in content:
                country = content.split('Страна происхождения')[-1].strip()
                code_dict = {'Страна происхождения': country}
                #print(code_dict)
                char_value = char_value | cont_dict
            count = 0
            #print('\n')
    list_name_char.append({goods_name: char_value})
    return list_name_char



driver.close()
