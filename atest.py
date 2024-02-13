from scr_maker.manager import make_screenshot
from excel_funcs import excel_to_dicts
from scr_maker.counter import counter_gen


''' Делаем только скриншоты ссылок
A: scr_num,
B: link
'''

screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
xlsx_folder_path = 'C:/Users/G.Tishchenko/Desktop/2 кв 2024/'
# xlsx_file_name = xlsx_folder_path + '26 Оборудование для театрально.xlsx'
# xlsx_file_name = xlsx_folder_path + '19 Бытовые приборы.xlsx'
# xlsx_file_name = xlsx_folder_path + '3 Нормирование.xlsx'
xlsx_file_name = xlsx_folder_path + '3 компьютерное.xlsx'

headers_names = [
    'Ссылка',
    'Номер скрина',
    'Цена',
]

sleep_time = 4

link_dicts = excel_to_dicts(
    xlsx_file_name,
    sheet_name = 'Лист2',
    headers_names = headers_names,
    headers = False
    )[:]

counter_obj = counter_gen(link_dicts)

for row in link_dicts:

    if not row['Цена']:
        img_name = screen_folder + f'{row["Номер скрина"]}.jpg'

        make_screenshot(img_name, row['Ссылка'], sleep_time = sleep_time)

    print(counter_obj.__next__(), end = '\r');
