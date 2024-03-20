'''

    загружаем файлы в СЭД:

    берет все файлы с 1 номером "1234_***"
    по номеру ворд файла ищет карточку в "сэд"
    загружает файл в карточку
    проверяет что такое имя существует на странице

    ps. перед применением обновить selenium driver
    ps. в строке 79 закомменчена ф-я встаки --> раскомемнтить

'''

import os
from ten_edit import *
from ten_edit_two import *
import time
# папка с файлами


DOC_FOLDER = 'C:/Users/G.Tishchenko/Desktop/файлы_сэд/Экранные копии/'
# DOC_FOLDER = 'C:/Users/G.Tishchenko/Desktop/файлы_сэд/Ответы на запрос/'
user_name, user_passw = 'Tishchenko_GL', 'cmec789'
# DOC_FOLDER = 'C:/Users/G.Tishchenko/Desktop/файлы_сэд/Ответы на запрос не мои/'
# user_name, user_passw = 'Mustafin_RI', '123123'

# инфа для формирования нофера источника "04-4129/23-0-0"
LEFT_PART = '04-'
RIGHT_PART = '/24-0-0'

docs = os.listdir(DOC_FOLDER)

# объединение файлов по 1 номеру
numbers = {}
for doc_name in docs:
    doc_name_split = doc_name.split('_')
    number = doc_name_split[0]
    full_number = LEFT_PART + number + RIGHT_PART
    doc_path = DOC_FOLDER + doc_name
    comp_name = ' '.join(doc_name_split[1:-2])

    if number in numbers.keys():
        numbers[number]['files'].append(doc_path)
    else:
        numbers[number] = {
            'files': [doc_path],
            'full_number': full_number,
            'comp_name': comp_name,
        }

# заходив в сэд
driver = get_driver()
authorization_func(driver, user_name, user_passw)


counter = 0
# загружаем файлы
for number, value in numbers.items():
    # вбиваем в поиск
    q = value['full_number']
    print('\nИщем', counter, q, value['comp_name'])
    find_document_from_main(driver, q)
    click_by_name(driver)
    counter += 1
    # if counter > 2:
    #     break
    cur_files = set()


    for file in value['files']:
        print('Добавляем', file)
        file_name = file.split('/')[-1]
        cur_files.add(file_name)

        ''' Добавление 2 '''
        # что бы проверить все загруженные файлы
        # надо закометить след строку
        # upload_file(driver, file)

    # up_files = set()
    for file_name in cur_files:
        is_doc_uploaded(driver, file_name)

    time.sleep(3)
    # while up_files | cur_files:
    #     up_files = get_uploaded_files(driver)

    # input('Когда добавиться нажать "Enter"')
    driver.get('http://srv07/cmec/CA/Desktop/Default.aspx')
driver.quit()
