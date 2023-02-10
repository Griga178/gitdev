'''ПОЛУЧАЕМ СПИОК КАТАЛОГА МАГАЗИНА xcom
'''
import requests
import re
from bs4 import BeautifulSoup
import openpyxl

main_p = "https://www.xcom-shop.ru"
cont_row = []

xcom_cat_url = "https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/kylery_i_sistemy_ohlazhdeniya/termopasta_termointerfeysy/"
cat_url_2 = "https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/kylery_i_sistemy_ohlazhdeniya/termopasta_termointerfeysy/?catalog=page-2"

def parse_xcom(cat_url):
    catalog_page = requests.get(cat_url)
    soup = BeautifulSoup(catalog_page.text, 'html.parser')

    container = soup.find_all("div", attrs = {"class": "catalog_items"})[0]
    for elem in container:
        if elem.name == "div":
            tag = elem.find_all("a")[1]
            link = tag.get("href")# ссылка по названию товара
            re_result = re.findall(r'\w+', tag.text)
            good_name = " ".join(re_result)
            cont_row.append([main_p + link, good_name])


for pg_num in range(2, 10):
    url = f"https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/kylery_i_sistemy_ohlazhdeniya/termopasta_termointerfeysy/?catalog=page-{pg_num}"
    print(f"Страница: {pg_num} \n")
    try:
        parse_xcom(url)
    except:
        print(f"Страница: {pg_num} - - - - -ОШИБКА")


exc_file = openpyxl.Workbook()
current_sheet = exc_file.active
current_sheet.title = "ЛИСТ1"

for row in cont_row:
    current_sheet.append(row)

exc_file.save("C:/Users/G.Tishchenko/Desktop/xcom_links.xlsx")
