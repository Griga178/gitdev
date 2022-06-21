'''
I Этап - автоматическая обработка

    Определяемся с кварталом

    Создаем все необходимые папки, рабочий файл с данными

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
import datetime
import sys
import os

current_date = datetime.datetime.now()
# first_qurter = datetime.strtime()
second_qurter =
third_qurter =
fourth_qurter =
print(current_date)



if len(sys.argv) > 1:
    print(sys.argv[1])

input_something = input("input ")

print('sleep 2 sec')
# time.sleep(2)
