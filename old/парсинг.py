import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from win10toast import ToastNotifier

# путь к драйверу и URL сайта
# yandex_driver_path = r'C:\Progs\yandexdriver.exe'
yandex_driver_path = r'yandexdriver.exe'
website_url = 'https://www.pepper.ru/new'
vandrouki_url = 'https://vandrouki.ru/'
pirates_travel_url = 'https://ru.pirates.travel/'


# создаем экземпляр драйвера для яндекс браузера, указывая путь к драйверу
options = Options()
options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path=yandex_driver_path)
browser = webdriver.Firefox()
# создаем объект для уведомлений
toaster = ToastNotifier()

# множество проверенных ссылок
checked_links = set()
driver.get(website_url)
# while True:
#     # открываем сайт
#     driver.get(website_url)
#
#     # ждем, пока страница загрузится
#     driver.implicitly_wait(10)
#
#     # получаем все элементы страницы с классом 'cept-tt thread-link linkPlain thread-title--list js-thread-title'
#     link_elements = driver.find_elements_by_css_selector('.cept-tt.thread-link.linkPlain.thread-title--list.js-thread-title')
#
#     # извлекаем атрибут 'href' и текст каждого элемента и добавляем в список в формате "текст - ссылка"
#     links = []
#     for element in link_elements:
#         title = element.text
#         url = element.get_attribute('href')
#         links.append(f"{title} - {url}")
#
#     # проверяем, есть ли новые ссылки
#     new_links = set(links).difference(checked_links)
#     if new_links:
#         # выводим список новых ссылок на экран и всплывающие уведомления
#         print('Новая скидка:')
#         for new_link in new_links:
#             checked_links.add(new_link)
#             print(new_link)
#             title, url = new_link.split(' - ', 1)
#             toaster.show_toast(title, url, duration=10, threaded=False)
#
#     # обновляем список проверенных ссылок
#     checked_links = set(new_links).union(checked_links)
#
#     # мониторинг vandrouki.ru
#     driver.get(vandrouki_url)
#     driver.implicitly_wait(10)
#     link_elements = driver.find_elements_by_css_selector('h2.entry-title a')
#     links = [f"{element.text} - {element.get_attribute('href')}" for element in link_elements]
#     new_links = set(links).difference(checked_links)
#     if new_links:
#         print('Новый пост на vandrouki.ru:')
#         for link in new_links:
#             checked_links.add(link)
#         print(link)
#         title, url = link.split(' - ')
#         toaster.show_toast(title, url, duration=10, threaded=True)
#     checked_links = set(new_links).union(checked_links)
#
#     # мониторинг ru.pirates.travel
#     driver.get(pirates_travel_url)
#     driver.implicitly_wait(10)
#     link_elements = driver.find_elements_by_css_selector('h2.post-title a')
#     links = [f"{element.text} - {element.get_attribute('href')}" for element in link_elements]
#     new_links = set(links).difference(checked_links)
#     if new_links:
#         print('Новый пост на ru.pirates.travel:')
#         for link in new_links:
#             checked_links.add(link)
#         print(link)
#         title, url = link.split(' - ')
#         toaster.show_toast(title, url, duration=10, threaded=True)
#     checked_links = set(new_links).union(checked_links)
#
#     # ждем 1 минуту и повторяем
#     time.sleep(30)
