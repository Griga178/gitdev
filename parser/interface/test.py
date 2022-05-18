from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'

options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
# options.add_argument('--headless')



# не ждем полной загрузки JS
caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
caps["pageLoadStrategy"] = "normal"
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

link1 = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
tag1 = ['span', 'class', 'ProductHeader__price-default_current-price']

link2 = 'https://www.kns.ru/product/telefon-panasonic-kx-ts2382ruw/'
link2_not_av = 'https://www.kns.ru/product/faks-panasonic-kx-fl423ruw/'
tag2 = ['span', 'class', 'price-org']
tag2_n = ['h1', 'itemprop', 'name']
tag_not_avaliable = ['div', 'class', 'goods-status'] # font-weight-bold mb-4

link3 = 'https://www.onlinetrade.ru/catalogue/smartfony-c13/zte/smartfon_zte_blade_a51_lite_2_32gb_zelenyy_zte_a51.lite.gn-2768952.html?utm_referrer=http%3a%2f%2f127.0.0.1%3a5000%2f'
tag3 = ['div', 'class', 'catalog__displayedItem__actualPrice']

def take_html_page(link):
    driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
    # wait = WebDriverWait(driver, 500)
    driver.get(link)
    child_xpath = '//div[@class="catalog__displayedItem__actualPrice"]'
    wait_elm = WebDriverWait(ancestor_element,10).until(EC.presence_of_element_located((By.XPATH, child_xpath)))
    # wait.until(EC.element_to_be_clickable((By.ID, "text")))
    html_page = driver.page_source

    driver.quit()
    return html_page

# Запуск:
html_string_page = take_html_page(link3)

three_tag_search(html_string_page, tag3)
