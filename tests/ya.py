import yaml
import openpyxl
from bs4 import BeautifulSoup
from ya_obj import Category

# replace("   ", " ")
# replace(": ", ":")

yaml_file = 'C:/Users/G.Tishchenko/Desktop/market_all.yml'
xlsx_file = 'C:/Users/G.Tishchenko/Desktop/market_all_cats.xlsx'

print("Открываем yaml файл...")
with open(yaml_file, "r", encoding='utf8') as stream:
    data = yaml.load(stream, Loader = yaml.FullLoader)

soup = BeautifulSoup(data, 'xml')
# print("Читаем xml содержимое - категории...")
# categories = soup.find_all("category")
#
# print("Обрабатываем категории...")
# for el in categories:
#     name = el.text
#     el_id = el.get("id")
#     parent_id = el.get("parentId") if el.get("parentId") else False
#     el_1 = Category(el_id, name, parent_id)
# else:
#     Category.check_connections()
#
# print("Сохраняем категории в excel файл...")
# wb = openpyxl.Workbook()
# sh1 = wb.active
# count = 0
# for key, item in Category.categories.items():
#     count += 1
#     sh1.append(item.get_list())
#     print(count, end = "\r")
# wb.save(xlsx_file)

offers = soup.find_all("offer")
for offer in offers:
    category_id = offer.categoryId.text
    g_id = offer.get("id")
    g_available = offer.get("available")
    g_link = offer.url.text
    g_name = offer.name.text
    g_price = offer.price.text
    print()
    # link = offer.get("url")
