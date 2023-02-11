import yaml
import openpyxl
from bs4 import BeautifulSoup
from ya_obj import Category

# desctop_path = 'C:/Users/G.Tishchenko/Desktop/'
desctop_path = 'C:/Users/Asus/Desktop/'
yaml_file = desctop_path + 'market_all3.yml'
xlsx_file = desctop_path + 'market_all_cats.xlsx'
print("Открываем файл...")
# yaml.warnings({'YAMLLoadWarning': False})
# with open(yaml_file, "r", encoding = 'utf8|') as stream:
with open(yaml_file, "r", encoding = 'utf8') as stream:
    # data = yaml.load(stream)
    # data = yaml.load(stream, Loader = yaml.FullLoader)
    data = yaml.load(stream, Loader = yaml.BaseLoader)
    # data = yaml.safe_load(stream)

    # try:
    #     data = yaml.load(stream, Loader = yaml.FullLoader)
    # except:
    #     print("Ошибки в записаном файле, исправляем...")
    #     stream.seek(0)
    #     count = 0
    #     with open(yaml_file + "1", "w+", encoding = 'utf8') as new_f:
    #         for line in stream:
    #             print(count, end = '\r')
    #             count += 1
    #             line = line.replace("\t", " ")
    #             line = line.replace(": ",":")
    #             # line = line.replace("-","")
    #             new_f.write(line)
    #     print("Запустить новый файл заново", yaml_file +"2")

print(data)
# soup = BeautifulSoup(data, 'xml')

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

# offers = soup.find_all("offer")
# for offer in offers:
#     category_id = offer.categoryId.text
#     g_id = offer.get("id")
#     g_available = offer.get("available")
#     g_link = offer.url.text
#     g_name = offer.name.text
#     g_price = offer.price.text
#     print()
    # link = offer.get("url")
