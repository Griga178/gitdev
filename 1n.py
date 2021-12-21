'''
На этом этапе формируется список ссылок в алфавитном порядке
с сохранением места ссылки в файле excel (список кортежей с 3 парам.).

из Excel в sorted_tuples

'''
import pandas

# Имя исходного файла
#exel_file = 'C:/Users/G.Tishchenko/Desktop/reestr 4.xlsx'
exel_file = 'C:/Users/G.Tishchenko/Desktop/reestr 2022 Обновленные ККН.xlsx'
# Имя исходного листа в файле
#sheets_name = 'new_kkn' #'RT new'
sheets_name = 'Norman'
# Имя столбца с сылками
column_links =  'Ссылка'
# Имя файла, куда будем сохранять
csv_file_name = 'C:/Users/G.Tishchenko/Desktop/R_1_2022.csv'
# Номер первой строки, в которой ссылка
first_num = 2

file = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_links])

# Список номеров строк (2,3,4,...) - для названия скриншотов
list_num = []
# список всех ссылок файла excel (со 2-ой строки до последней)
list_link = file[column_links].tolist()
# Заполнение списка со строками
for num in range(len(list_link)):
    list_num.append(num + first_num)
# список списков (Главная стр. номер строки, ссылка)
list_tuples_links = []
inde_x = 0
first_row_num = 2 # имя скриншота

# проверка на длинну списков (Не нужна)
if len(list_num) == len(list_link):

    for val in list_link:
        # вывод номера строки - названия скриншота
        print(first_row_num)
        # вырезаем главную стр из ссылки для сортировки
        try:
            # если в ячейке больше 2 ссылок с '\n' берем только первую
            if '\n' in val and type(val) == str:
                val = val.split("\n")[0] # убираем места с двумя ссылками
            # названия главной страницы
            main_page = (val.split("/")[2])
            # добавление в общий список: Главная стр. номер строки, ссылка
            list_tuples_links.append((main_page, first_row_num, val)) # list_num[inde_x]
        except:
            #return
            print('trouble with main_page')
        inde_x += 1
        first_row_num += 1
# сортировка списка по главной странице
sorted_tuples = sorted(list_tuples_links)
# Запись списка в файл
with open(csv_file_name, 'w') as file:
    for line in sorted_tuples:
        #if line[0] == 'my-shop.ru': # Для записи только 1 ссылок
            #file.write(f'{line[0]};{line[1]};{line[2]}\n')
        file.write(f'{line[0]};{line[1]};{line[2]}\n') # для записи всего
        #print(f'{line[0]};{line[1]};{line[2]}')
