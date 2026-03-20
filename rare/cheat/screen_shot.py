# screen_shot.py
import pyautogui
import numpy as np
import cv2

import os
import shutil

def edit_screen(old_name: str) -> bool:
    '''     Обновление даты создания скриншота     '''

    # загрузка старого скрина
    base_img = cv2.imread(old_name)
    # изменение старого скрина
    height, width = base_img.shape[:2]

    diff_height = 1080 - height
    diff_width = 1920 - width

    if diff_height >= 0 and diff_width >= 0:
        # делаем скрин нижней части экрана
        time_part = pyautogui.screenshot(region = (1800, 1040, 120-diff_width, 40-diff_height))
        time_part = cv2.cvtColor(np.array(time_part), cv2.COLOR_RGB2BGR)
        base_img[1040: height:, 1800: width, :3] = time_part

    else:
        print(old_name)
        print(height, width)
        return False

    cv2.imwrite(old_name, base_img)

    return True

def show_img(name: str):
    image = cv2.imread(name)
    cv2.imshow('image', image)
    cv2.waitKey(0)
