'''
    7n + 8n
    закидываем скриншоты в ворд файлы
    1 чтение рабочей таблицы, отбираем строки с ценами и скринами
    2 обработка информации:
        объединяем скрины по компаниям и типам источников
    3 создание папок для хранения .doc файлов
    4 создание .doc файлов

    название папки со скринами добавляется в название файла.doc
    "СИТИЛИНК ООО_компьютерное оборудование.doc"
'''
from excel_funcs import excel_to_list
from nine_editor import edit_row_v2

import os
import re
import docx
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

# - - - * - -  НАСТРОЙКИ ЕКСЕЛЬ ФАЙЛА - - - * - - -
EXCEL_FOLDER_PATH = 'C:/Users/G.Tishchenko/Desktop/3 кв 23/'
SCREEN_FOLDER_PATH = 'Z:/Тищенко Г.Л/3 кв 2023 скрины/'

EXCEL_FOLDER_PATH = EXCEL_FOLDER_PATH + '26 Оборудование для театрально.xlsx'
SCREEN_FOLDER_NAME = 'театральное оборудование'
SCREEN_FOLDER = SCREEN_FOLDER_PATH + SCREEN_FOLDER_NAME + "/"

# EXCEL_FOLDER_PATH = excel_folder + '19 Бытовые приборы.xlsx'
# SCREEN_FOLDER = scr_fldr_parent + 'бытовое оборудование/'

# EXCEL_FOLDER_PATH = excel_folder + '3 компьютерное.xlsx'
# SCREEN_FOLDER = scr_fldr_parent + 'компьютерное оборудование/'

# EXCEL_FOLDER_PATH = excel_folder + '3 Нормирование.xlsx'
# SCREEN_FOLDER = scr_fldr_parent + 'нормирование/'

FOLDER_PATH = 'C:/Users/G.Tishchenko/Desktop/файлы_сэд/'

ex_set = {
    'sheet_name': 'Лист1',
    'headers': False,
    'headers_names': [
        'Наименование ККН',
        'Источник ценовой информации',
        'ИНН поставщика',
        'Наименование поставщика',
        'Номер скрина',
        'Новая цена',
    ]
}

def edit_company_name(comp_name):

    re_sult = re.findall(r'\w+', comp_name.upper())
    return "_".join(re_sult)

def edit_row(exel_row, prev_row = False):
    # Обработка строк
    # Условия для проверки скрина
    screen_name = exel_row[4]
    if prev_row:
        kkn_name = exel_row[0] if exel_row[0] else prev_row['kkn_name']
        # print(kkn_name, screen_name) if kkn_name else print('kknssssssssssssssssssssssname')
    else:
        kkn_name = exel_row[0]
    print(screen_name, kkn_name)
    source = exel_row[1]
    company_inn = exel_row[2]
    company_name = exel_row[3]
    price = exel_row[5]

    try:

        if source[0].upper() == 'О':
            source_type = "Ответ на запрос"
            spl_row = source.split("-")
            source_type_number = spl_row[1][:-3]
        elif source[0].upper() == 'Э':
            source_type = "Экранная копия"
            spl_row = source.split("-")
            source_type_number = spl_row[1][:-3]
        else:
            source_type = None
    except:
        return None


    if price and screen_name:
        return {
            'kkn_name': kkn_name,
            'source': source,
            'source_type': source_type,
            'source_type_number': source_type_number,
            'company_name': edit_company_name(company_name),
            'company_inn': company_inn,
            'screen_name': SCREEN_FOLDER + str(screen_name) + ".jpg",
            'screen_number': screen_name,
            'price': price,
        }

def combine_info(ex_list):
    information = {
        'Экранные копии': {},
        'Ответы на запрос': {}
    }
    prev_row = False
    for el in ex_list:
        row = edit_row(el, prev_row)
        prev_row = row
        if row:
            if row['source_type'] == "Экранная копия":
                if row['company_name'] in information['Экранные копии'].keys():
                    # information['Экранные копии'][row['company_name']]['screens'].append(row['screen_name'])
                    information['Экранные копии'][row['company_name']]['screens'].append({"path": row['screen_name'], "name": row['screen_number']})
                else:
                    information['Экранные копии'][row['company_name']] = {
                        # 'screens': [row['screen_name']],
                        'screens': [{"path": row['screen_name'],
                                    "name": row['screen_number'],
                                    'kkn_name': row['kkn_name']}],
                        'number': row['source_type_number'],
                        'company_name': row['company_name'],

                        }
            elif row['source_type'] == "Ответ на запрос":
                if row['company_name'] in information['Ответы на запрос'].keys():
                    # information['Ответы на запрос'][row['company_name']]['screens'].append(row['screen_name'])
                    information['Ответы на запрос'][row['company_name']]['screens'].append({"path": row['screen_name'], "name": row['screen_number']})
                else:
                    information['Ответы на запрос'][row['company_name']] = {
                        # 'screens': [row['screen_name']],
                        'screens': [{"path": row['screen_name'],
                                    "name": row['screen_number'],
                                    'kkn_name': row['kkn_name']}],
                        'number': row['source_type_number'],
                        'company_name': row['company_name'],

                        }

    return information

def create_folders():
    try:
        os.mkdir(FOLDER_PATH)
    except:
        print('Главные папка уже есть')
    try:
        os.mkdir(FOLDER_PATH + 'Ответы на запрос')
    except:
        print('Ответы на запрос - папка уже есть')
    try:
        os.mkdir(FOLDER_PATH + 'Экранные копии')
    except:
        print('Экранные копии - папка уже есть')

def create_doc_test(file_path, comp_info):
    page_header = comp_info['number'] + ' ' + comp_info['company_name']
    images = comp_info['screens']
    print("\n\nФайл:", file_path)
    print('колонтитул:', page_header)
    for image in images:
        print("подпись", image['kkn_name'])
        print("Скрин", image['path'])

def create_doc(file_path, comp_info):
    images = comp_info['screens']
    page_header = comp_info['number'] + ' ' + comp_info['company_name']
    # Создаем word файл
    document = docx.Document()
    section = document.sections[0]
    # Горизонтальный формат листа
    new_width, new_height = section.page_height, section.page_width
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = new_width
    section.page_height = new_height
    # отступы на странице
    section.top_margin = Inches(0.75)
    section.left_margin = Inches(0.7)
    # добавление верхнего колониткула
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.text = page_header

    # Закидываем в word файл скриншоты
    pic_number = 0
    try:
        for image in images:
            pic_number += 1
            # имя существующего скриншота
            try:
                document.add_picture(image['path'], width = docx.shared.Inches(9.3), height = docx.shared.Inches(6.5))
                pic_number += 1
            except:
                print(image['path'], "не найти")

        document.save(file_path)
        print(f'{file_path} - сохранен, скриншотов: {pic_number}')
    except:
        print(f' Нарушен стандарт в: {page_header}')


def save_screens(information, logs = True):
    screen_amount_all = 0
    company_amount_all = 0

    for key, val in information.items():
        print('Определяем имя папки:', key, end = '\n\n') if logs else None
        screen_amount = 0
        company_amount = 0
        for comp_name, comp_info in val.items():
            file_name = FOLDER_PATH + key + '/' + comp_info['number'] + '_'+ comp_name + '_' + SCREEN_FOLDER_NAME + '.docx'
            print('\n', file_name) if logs else None
            company_amount += 1
            company_amount_all += 1
            screen_amount_cur = 0

            # create_doc(file_name, comp_info)
            create_doc_test(file_name, comp_info)
            # for scrname in comp_info['screens']:
            #     screen_amount_cur += 1
            #     screen_amount_all += 1
            #     print('- - - >', scrname[-10:]) if logs else None
            # else:
            #     print(f'- - > Скринов: {screen_amount_cur}') if logs else None
            # screen_amount += screen_amount_cur

    #     else:
    #         print(f'\nСкринов: {screen_amount}\nКомпаний: {company_amount}') if logs else None
    #
    # else:
    #     print(f'\nВсего:\nСкринов: {screen_amount_all}\nКомпаний: {company_amount_all}')

create_folders()
ex_list = excel_to_list(EXCEL_FOLDER_PATH, **ex_set)
information = combine_info(ex_list)

save_screens(information, logs = False)
