from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import time

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'

options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
options.add_argument('--headless')



# не ждем полной загрузки JS
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
# caps["pageLoadStrategy"] = "normal"
# Разные варианты поиска цены

# Поиск по 3 тегам - есть
def three_tag_search(html_string_page, tag):
    soup = BeautifulSoup(html_string_page, 'html.parser')
    print(soup, '\n\n')
    # result_info = soup.find(tag[0], {tag[1], tag[2]})
    # result_info = soup.find('h1', itemprop = 'name')
    result_info = soup.find(tag[0], attrs={tag[1]: tag[2]})
    # print(result_info.text)

# Поиск Сообщения нет в наличии
# Настройка у магазинов для статусов товара

status_not_avaliable = 'Нет в наличии'
status_avaliable = 'В наличии'
status_other = 'Предзаказ'

defender_message = ['h1', 'Проверка безопасности']

manual_mode = True

def take_html_page(link, tag, num = False):

    driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
    # driver = webdriver.Chrome(desired_capabilities = caps, options = options)
    driver.set_window_size(1920, 1080)
    driver.get(link)


    # child_xpath = f'//{tag[0]}[@{tag[1]}="{tag[2]}"]'
    child_xpath = f'//{tag[0]}[contains(@{tag[1]}, "{tag[2]}")]'
    try:
        time.sleep(3)
        try:
            def_wait_elm = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//h1[text() = "Проверка безопасности"]')))
            print("Проверка безопасности")
            driver.quit()
            print('вышли из др.')
            options.headless = False
            print('настройки фолс.')
            driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
            print('настройки сохранили')
            driver.get(link)
        except:

            print('не нашли форму безопасности')
        wait_elm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, child_xpath)))
        html_page = driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        content = soup.find(tag[0], attrs={tag[1]: tag[2]})
        # content = wait_elm.get_attribute('innerHTML')
    except:
        print(driver.page_source)
        content = 'ДОЛГО ЖДАТЬ!'

    # print([wait_elm.text])
    print([content])
    # wait.until(EC.element_to_be_clickable((By.ID, "text")))
    #

    driver.quit()
    # return html_page





def tester():
    num = 0
    start_time = time.time()
    link1 = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
    tag1 = ['span', 'class', 'ProductHeader__price-default_current-price']

    link2 = 'https://www.kns.ru/product/telefon-panasonic-kx-ts2382ruw/'
    link2_not_av = 'https://www.kns.ru/product/faks-panasonic-kx-fl423ruw/'
    tag2 = ['span', 'class', 'price-org']
    tag2_n = ['h1', 'itemprop', 'name']
    tag_not_avaliable = ['div', 'class', 'goods-status'] # font-weight-bold mb-4

    link3 = 'https://www.onlinetrade.ru/catalogue/smartfony-c13/zte/smartfon_zte_blade_a51_lite_2_32gb_zelenyy_zte_a51.lite.gn-2768952.html'
    tag3 = ['div', 'class', 'catalog__displayedItem__actualPrice']

    # УСПЕХ:
    print('# 1')
    take_html_page(link1, tag1, 1)
    # УСПЕХ:
    print('# 2')
    take_html_page(link2, tag2, 2)
    print('# 3')
    take_html_page(link2, tag2_n, 3)
    print('# 4')
    take_html_page(link2_not_av, tag_not_avaliable, 4)
    # УСПЕХ:
    # Надо ждать загрузки JS дольше обычного, используя "wait"
    print('# 5')
    take_html_page(link3, tag3, 5)

    cur_sec = round((time.time() - start_time), 2)
    print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')

tester()
