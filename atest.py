from scr_maker.manager import make_screenshot
from excel_funcs import excel_to_dicts
from scr_maker.counter import counter_gen


''' Делаем только скриншоты ссылок
с "Лист2"
A: scr_num,
B: link
screen_folder - куда сохранять скриншот
xlsx_folder_path - где файл рабочей таблицы
xlsx_file_name - название рабочей таблицы
'''

screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
xlsx_folder_path = 'C:/Users/G.Tishchenko/Desktop/3 кв 2025/'
# xlsx_file_name = xlsx_folder_path + '26 Оборудование для театрально.xlsx'
# xlsx_file_name = xlsx_folder_path + '19 Бытовые приборы.xlsx'
xlsx_file_name = xlsx_folder_path + 'Нормирование.xlsx'
# xlsx_file_name = xlsx_folder_path + '3 компьютерное.xlsx'
# xlsx_file_name = xlsx_folder_path + 't.xlsx'
# Разовая акция
# xlsx_folder_path = 'C:/Users/G.Tishchenko/Desktop/'
# xlsx_file_name = xlsx_folder_path + 'Рабочая таблица 3.0.xlsx'


headers_names = [
    'Ссылка',
    'Номер скрина',
    'Цена',
]

sleep_time = 5

link_dicts = excel_to_dicts(
    xlsx_file_name,
    sheet_name = 'Лист2',
    headers_names = headers_names,
    headers = False
    )

link_dicts_v2 = []
# для корректного отображения оставшегося времени
for row in link_dicts:
    if not row['Цена']:
        link_dicts_v2.append(row)

print(f'Всего ссылок {len(link_dicts_v2)} шт.')
link_dicts_v2 = link_dicts_v2[:300] # сокращаем список
counter_obj = counter_gen(link_dicts_v2)

for row in link_dicts_v2:
    # if not row['Цена']:
    img_name = screen_folder + f'{row["Номер скрина"]}.jpg'
    make_screenshot(img_name, row['Ссылка'], sleep_time = sleep_time)
    print(counter_obj.__next__(), end = '\r');
