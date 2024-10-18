import pyautogui
import numpy as np
import cv2

import os
import shutil

def edit_screen(old_name: str, new_name: str) -> None:
    '''     Обновление даты создания скриншота     '''

    # загрузка старого скрина
    base_img = cv2.imread(old_name)
    # изменение старого скрина
    height, width = base_img.shape[:2]
    standart_h = 1080
    standart_w = 1920
    d_h = standart_h - height
    d_w = standart_w - width
    print(d_h, d_w)

    # скриншот нижнего правого угла
    # time_part = pyautogui.screenshot(region = (1800, 1040, 120, 40))
    time_part = pyautogui.screenshot(region = (1800, 1040+d_h, 120, 40-d_h))
    time_part = cv2.cvtColor(np.array(time_part), cv2.COLOR_RGB2BGR)
    # print(time_part.shape)
    # base_img[1040 - d_h: 1080 - d_h:, 1800 - d_w: 1920, :3] = time_part
    # ВОЗМОЖНО - использовать когда base_img съехал на 1 пикс наверх
    # base_img[1041 - d_h: height:, 1800 - d_w: width, :3] = time_part
    base_img[1040 - d_h: height:, 1800 - d_w: width, :3] = time_part


    if new_name:
        cv2.imwrite(new_name, base_img)
    else:
        cv2.imwrite(old_name, base_img)


def show_img(name: str):
    image = cv2.imread(name)
    cv2.imshow('image', image)
    cv2.waitKey(0)

def copy_image(old_name: str, new_name: str) -> None:
    shutil.copy(old_name, new_name)

def del_image(name: str) -> None:
    os.remove(name)

def check(name: str) -> bool:
    return os.path.exists(name)
