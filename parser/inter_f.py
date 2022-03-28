from save_load import *
print("Hello World!")

file_name = 'comon_set.pkl'
input_history = []
try:
    set_for_pickle = pkl_set_reader(file_name)
except:
    print('no file')
    set_for_pickle = set()

def begin(text):


    input_history.append(text)
    stop_text = {'stop', 's', 'break', 'quit'}
    show_funcs = {'0', 'help'}
    show_shop = {'shop', 'Shop', '1'}
    if text in stop_text:
        pkl_saver(file_name, set_for_pickle)
        print('pickle - saved... Buy!')
        exit()
    elif text in show_shop:
        print('www.citilink.ru')

    elif text in show_funcs:
        print('''0 для списка команд
1 показать доступные магазины
2 история ввода
3 сохранить строку в множество
4 сохранить строку в множество''')

    elif text == '2':
        print(input_history)
    elif text == '3':
        set_for_pickle.add(text)
    elif text == '4':
        print(set_for_pickle)
    print("Делаю что-то еще")
    print("- - - ")
    begin(str(input("\nВведите команду: ")))



begin(str(input("Начало работы\nВведите команду: ")))
