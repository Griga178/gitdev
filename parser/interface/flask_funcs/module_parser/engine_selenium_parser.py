from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from flask_funcs.module_parser.engine_beauty_parser import html_searcher

def run_selenium_parser(settings):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
    options.add_argument('--headless')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    # proxy = "144.240.187.80:83"
    # caps["proxy"] = {"httpProxy":proxy,
    #    "ftpProxy": proxy,
    #    "sslProxy": proxy,
    #    "noProxy": None,
    #    "proxyType":"MANUAL",
    #    "class":"org.openqa.selenium.Proxy",
    #    "autodetect": False
    #   }

    binary_yandex_driver_file = 'yandexdriver.exe'

    headless_mode = settings['headless_mode']
    if not headless_mode:
        options.headless = False

    driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
    driver.delete_all_cookies()
    # driver = webdriver.Chrome(desired_capabilities = caps, options = options)

    dict_output = {}
    for link_id, link in settings['links'].items():
        link_result = {}
        tag_setting = settings['tag_setting']
        try:
            driver.get(link)
            child_xpath = f'//body[contains(text(), "")]'
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, child_xpath)))
            # import time
            # print('sleep 5')
            # time.sleep(5)
            html_page = driver.page_source
            link_result = html_searcher(tag_setting, html_page)
        except:
            dict_output[link_id] = False
            break
        dict_output[link_id] = link_result

    driver.quit()

    return dict_output
