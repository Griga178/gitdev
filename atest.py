from scr_maker.manager import start_screening

''' Делаем только скриншоты ссылок'''
screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/all_2023_1.xlsx'
start_screening(xlsx_file_name, screen_folder, sleep_second = 3, sheet_name = 'cur_parse')
