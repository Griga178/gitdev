'''
На этом этапе формируется список ссылок в алфавитном порядке
с сохранением места ссылки в файле excel (список кортежей с 3 парам.).

из Excel в sorted_tuples

'''
import pandas

# Имя исходного файла
# exel_file = 'C:/Users/G.Tishchenko/Desktop/Нормирование.xlsx'
# exel_file = 'C:/Users/G.Tishchenko/Desktop/10_ч.xlsx'
exel_file = 'C:/Users/G.Tishchenko/Desktop/norm_4.xlsx'
# Имя исходного листа в файле
# sheets_name = '(177 шт) (Перечень)'
sheets_name = 'main'
# Имя столбца с сылками
column_links =  'Ссылка'
# Имя столбца с номерами для скриношотов
screen_nums = 'Номер скриншота'
# Имя файла, куда будем сохранять
csv_file_name = 'C:/Users/G.Tishchenko/Desktop/norm_4.csv'
# Номер первой строки, в которой ссылка
first_num = 2

file = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_links, screen_nums])


# список всех ссылок файла excel (со 2-ой строки до последней)
list_link = file[column_links].tolist()
list_scr_name = file[screen_nums].tolist()

# список списков (Главная стр. номер строки, ссылка)
list_tuples_links = []

trouble_link = 0
for el_num in range(len(list_link)):
    val = list_link[el_num]
    try:
        # если в ячейке больше 2 ссылок с '\n' берем только первую
        if '\n' in val and type(val) == str:
            val = val.split("\n")[0] # убираем места с двумя ссылками
        # названия главной страницы
        main_page = (val.split("/")[2])
        # добавление в общий список: Главная стр. номер строки, ссылка
        list_tuples_links.append((main_page, int(list_scr_name[el_num]), val)) # list_num[inde_x]
    except:
        print(list_scr_name[el_num], end = ' ')
        print('trouble with main_page', val)
        trouble_link += 1
print("ссылок с ошибкой", trouble_link)

# сортировка списка по главной странице
sorted_tuples = sorted(list_tuples_links)
# Запись списка в файл
with open(csv_file_name, 'w') as file:
    for line in sorted_tuples:
        #if line[0] == 'my-shop.ru': # Для записи только 1 ссылок
            #file.write(f'{line[0]};{line[1]};{line[2]}\n')
        file.write(f'{line[0]};{line[1]};{line[2]}\n') # для записи всего
        #print(f'{line[0]};{line[1]};{line[2]}')
