from browser import open_page
from screen import make_screen
from excel import read_xlsx
from counter import counter_gen

import time, pyautogui

# setts
screen_folder = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
xlsx_file_name = 'C:/Users/G.Tishchenko/Desktop/запчасти.xlsx'
sleep_second = 5

link_list = read_xlsx(xlsx_file_name, sheet_name = 'cur_parse')
counter_obj = counter_gen(link_list)

for scr_num, link in link_list:
    img_name = screen_folder + f'{scr_num}.jpg'
    open_page(link)
    time.sleep(sleep_second)
    make_screen(img_name)
    pyautogui.hotkey('ctrl', 'w')
    print(counter_obj.__next__(), end = '\r')
