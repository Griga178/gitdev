from scr_maker.browser import open_page
from scr_maker.screen import make_screen
from scr_maker.excel import read_xlsx
from scr_maker.counter import counter_gen

import time, pyautogui

def start_screening(xlsx_file_name, screen_folder, sleep_second = False, sheet_name = False):
    link_list = read_xlsx(xlsx_file_name, sheet_name if sheet_name else False)
    counter_obj = counter_gen(link_list)

    for scr_num, link in link_list:
        img_name = screen_folder + f'{scr_num}.jpg'
        open_page(link)
        time.sleep(sleep_second)
        make_screen(img_name)
        pyautogui.hotkey('ctrl', 'w')
        print(counter_obj.__next__(), end = '\r')


# screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
# xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/all_2023_1.xlsx'
# start_screening(xlsx_file_name, screen_folder, sleep_second = 2, sheet_name = 'cur_parse'):
