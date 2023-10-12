from scr_maker.browser import open_page
from scr_maker.screen import make_screen
# from scr_maker.counter import counter_gen
# from scr_maker.excel import read_xlsx


import time, pyautogui

def make_screenshot(img_name, link, sleep_time = 3):

    meta_content = {"link": link}

    open_page(link)
    time.sleep(sleep_time)
    make_screen(img_name, meta_content)
    pyautogui.hotkey('ctrl', 'w')


# Запускаемый файл
# ../atest.py
