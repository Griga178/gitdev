import time

first_mesage = '''
заружено ссылок {500} шт.
количество компаний(их настройки) {50(30)}
информация по компаниям {50/30}
'''

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
        run_console_interface(0)
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
