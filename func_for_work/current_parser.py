import openpyxl

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

binary_yandex_driver_file = 'yandexdriver.exe'


import requests
from bs4 import BeautifulSoup

import numpy as np
import pyautogui
import imutils
import cv2


# import pickle

start_time = time.time()

# читаем настройки для парсера
# - словарь настроек
#
#
# читаем ссылки которые будем парсить
# -список ссылок (отсортированные опр. образом)
#
# итератор
# -сохранение цены в xlsx при удачном парсинге
# -сохраниение скриншота
