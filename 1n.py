'''
Формируется список списков в алфавитном порядке
с сохранением места ссылки в файле excel (список кортежей с 3 парам.).

из Excel в sorted_list

'''
from my_excel.excel_funcs import excel_to_list
from my_folder.folder_funcs import check_file_name
# Имя исходного файла
# exel_file = 'C:/Users/G.Tishchenko/Desktop/Нормирование.xlsx'
# exel_file = 'C:/Users/G.Tishchenko/Desktop/10_ч.xlsx'
exel_file = 'C:/Users/G.Tishchenko/Desktop/19p_4.xlsx'
# Имя исходного листа в файле
sheets_name = 'main'
# Имя файла, куда будем сохранять
csv_file_name = 'C:/Users/G.Tishchenko/Desktop/sort_links.csv'
csv_file_name = check_file_name(csv_file_name)

excel_list = excel_to_list(exel_file, sheet_name = sheets_name, headers_names = ['Ссылка', 'Номер скриншота'], headers = False)

list_tuples_links = []
trouble_link = 0
for el_num in excel_list:
    # val = list_link[el_num]
    val = el_num[0]
    try:
        # если в ячейке больше 2 ссылок с '\n' берем только первую
        if '\n' in val and type(val) == str:
            val = val.split("\n")[0] # убираем места с двумя ссылками
        # названия главной страницы
        main_page = (val.split("/")[2])
        # добавление в общий список: Главная стр. номер строки, ссылка
        list_tuples_links.append((main_page, int(el_num[1]), val)) # list_num[inde_x]
    except:
        print(el_num[1], end = ' ')
        print('trouble with main_page', val)
        trouble_link += 1
print("ссылок с ошибкой", trouble_link)

# сортировка списка по главной странице
sorted_tuples = sorted(list_tuples_links)

# # Запись списка в файл
with open(csv_file_name, 'w') as file:
    for line in sorted_tuples:
        file.write(f'{line[0]};{line[1]};{line[2]}\n') # для записи всего
