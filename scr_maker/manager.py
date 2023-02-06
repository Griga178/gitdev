from scr_maker.browser import open_page
from scr_maker.screen import make_screen
from scr_maker.excel import read_xlsx
from scr_maker.counter import counter_gen

import time, pyautogui

def start_screening(xlsx_file_name, screen_folder, sleep_second = False, sheet_name = False):
    link_list = read_xlsx(xlsx_file_name, sheet_name) # if sheet_name else False
    # excel_data = my_func(xlsx_file_name, sheet_name)
    counter_obj = counter_gen(link_list)

    for scr_num, link,  p, kkn_name in link_list[350:600]: # нормирование
        meta_content = {"id": scr_num, "link": link, "kkn": kkn_name}
        img_name = screen_folder + f'{scr_num}.jpg'
        open_page(link)
        time.sleep(sleep_second)
        make_screen(img_name, meta_content)
        pyautogui.hotkey('ctrl', 'w')
        print(counter_obj.__next__(), end = '\r');

# Запускаемый файл
# ../atest.py
