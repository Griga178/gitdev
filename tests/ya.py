import yaml
import openpyxl
from bs4 import BeautifulSoup
from ya_obj import Category
from xcom_offer import Offer
from xcom_offer import File_creator

desctop_path = 'C:/Users/G.Tishchenko/Desktop/'
# desctop_path = 'C:/Users/Asus/Desktop/'
yaml_file = desctop_path + 'market_all2.yml'
xlsx_file = desctop_path + 'xcom2/m_all_cats.xlsx'
print("Открываем файл...")
# yaml.warnings({'YAMLLoadWarning': False})
# with open(yaml_file, "r", encoding = 'utf8|') as stream:
with open(yaml_file, "r+", encoding = 'utf8') as stream:
    # data = yaml.load(stream, Loader = yaml.BaseLoader)
    # data = yaml.safe_load(stream)
    # data = yaml.load(stream, Loader = yaml.FullLoader)
    # try:
    #     data = yaml.load(stream, Loader = yaml.FullLoader)
    # except:
    #     print("Ошибки в записаном файле, исправляем...")
    #     stream.seek(0)
    #     file_lines = []
    #     count = 0
    #     for line in stream:
    #         print(count, end = '\r')
    #         count += 1
    #         line = line.replace("\t", " ")
    #         line = line.replace(": ",":")
    #         line = line.replace("# ","№ ")
    #         line = line.replace(" №"," №")
    #         file_lines.append(line)
    #     else:
    #         print('\n')
    #
    #     stream.seek(0)
    #     count = 0
    #     print("Перезаписываем...")
    #     for line in file_lines:
    #         print(count, end = '\r')
    #         count += 1
    #         stream.write(line)
    #     else:
    #         print('\n')
    #     stream.seek(0)
    #     print("Запускаем новый файл заново", yaml_file)
    #     data = yaml.load(stream, Loader = yaml.FullLoader)

    soup = BeautifulSoup(stream.read(), 'xml')

print("Читаем xml содержимое - категории...")
categories = soup.find_all("category")

print("Обрабатываем категории...")
for el in categories:
    name = el.text
    el_id = el.get("id")
    parent_id = el.get("parentId") if el.get("parentId") else False
    el_1 = Category(el_id, name, parent_id)
else:
    Category.check_connections()
#
print("Сохраняем категории в excel файл...")
wb = openpyxl.Workbook()
sh1 = wb.active
count = 0
for key, item in Category.categories.items():
    count += 1
    sh1.append(item.get_list())
    print(count, end = "\r")
wb.save(xlsx_file)
print("Читаем xml содержимое - предложения...")
offers = soup.find_all("offer")
offer_list = []
for offer in offers:
    # print(offer)
    o = Offer(
        id = offer.get("id"),
        available = offer.get("available"),
        url = offer.url.text,
        categoryId = offer.categoryId.text,
        name = offer.find('name').text,
        price = offer.price.text if offer.price else False,
        vendor = offer.vendor.text if offer.vendor else False,
        model = offer.model.text if offer.model else False,
        vendorCode = offer.vendorCode.text if offer.vendorCode else False,
        description = offer.description.text if offer.description else False
    )
    offer_list.append(o)
    # print(o)

print(len(offer_list))

f_c = File_creator(Category.categories)
for offer in offer_list:
    f_c.add_offer_category(offer)

f_c.create_files()
