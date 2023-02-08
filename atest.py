from scr_maker.manager import start_screening

''' Делаем только скриншоты ссылок'''

screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
# xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/19 Бытовые приборы.xlsx'
# xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/26 Оборудование для театрально.xlsx'
xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/3 компьютерное.xlsx'
# xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/3 Нормирование2.xlsx'


start_screening(xlsx_file_name, screen_folder, sleep_second = 5, sheet_name = 'Номера ссылок')
