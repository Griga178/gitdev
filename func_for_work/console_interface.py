import time

second_mesage = '''
1   - Запустить парсер
2   - Прверка скринов
3   - Ручной парсинг
4   - Добавление скринов в word - файл
5   - Добавление word в Сэд
    - Проверка компаний по ИНН
0   - Выход из программы
'''

def run_console_interface(command = False):
    print('Панель управления')
    if not command:
        # print(first_mesage)
        # print(second_mesage)
        command = str(input("Ввести цифру: "))
        run_console_interface(command)

    elif command == "0":
        print("Good bye")
        time.sleep(1)
        quit()
    elif command == "1":
        print("Включаем парсер")
        run_console_interface()
    elif command == "2":
        print("Провеяем скрины")
        run_console_interface()
    elif command == "3":
        print("Ручной парсинг")
        run_console_interface()
    elif command == "4":
        print("Добавляем скрины в ворд")
        run_console_interface()
    elif command == "9":
        print("помощь")
        run_console_interface()

def run_parser_interface():
    print("Парсер запущен")
    print(' 1 - для проверки ссылки')
    # ФУНКЦИИ:
    # 1 ПРОПАРСИТЬ НОВЫЕ ССЫЛКИ
    # 2 ПРОВЕРИТЬ КОНКРЕТНУЮ ССЫЛКУ
