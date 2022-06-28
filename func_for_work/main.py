'''
I Этап - автоматическая обработка

    Создаем все необходимые папки, рабочий файл с данными

    читаем excel-файл
        Источники (открытые/закрытые)
        Номер части
        Ссылки
        ...

    меняем рабочую таблицу - добавляем номера скриншотов

    выгружаем номер скрина - ссылка

    парсим ссылки, сохраняем скрины

II Этап - проверка, ручной парсинг
    проверка скриншотов, цен
    проход по оставшимся ссылкам запись - скрин

    ручная работа с файлом, поиск новых ссылок

III Этап - сохранение, загрузка в СЭД

    выгружаем список компаний

    связь с номерами ответов/экранок

    загрузка скриншотов в file.docx

    загрузка docx в сэд

    проверка

    загрузка всех файлов в общую папку
'''

import time
import sys
import os

from folders import run_manager
from excel_reader import read_work_table


run_manager()

if len(sys.argv) > 1:
    print(sys.argv[1])
    a = read_work_table(sys.argv[1])
    # print(a)



input_something = input("input ")

print('sleep 2 sec')
# time.sleep(2)


def define_date():
    quarters = ["01", "02", "03", "04"]
    print("Какой квартал: ", ", ".join(quarters))
    chosen_qu = int(input("Введите от 1 - 4: "))
    chosen_year = str(input("За какой год: "))
    current_date = f'{quarters[chosen_qu - 1]}_{chosen_year}'
    return current_date
