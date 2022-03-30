from save_load import *
print("Hello World!")

file_name = 'comon_set.pkl'


try:
    set_for_pickle = pkl_set_reader(file_name)
except:
    print('no file')
    set_for_pickle = set()

help_desk = '''Помощь (для вызова - "h")
'''

def begin(text = False):
    if not text:
        text = str(input("Начало работы\nВведите команду: "))


    if text == "0":
        print('Выход из программы!')
        exit()
    elif text == "1":
        print("Зашли в ПАРСЕР")
    elif text == '2':
        print("Зашли в БД")

    begin()



begin()

# БУДЕМ ДЕЛАТЬ PYQT
