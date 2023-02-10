catalog_page_url = "https://www.citilink.ru/catalog/termopasta/"
catalog_page_url_dns = "https://www.dns-shop.ru/catalog/17a9cccc16404e77/termointerfejsy/"
catalog_page_url_xcom = "https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/kylery_i_sistemy_ohlazhdeniya/termopasta_termointerfeysy/"
from bs4 import BeautifulSoup
import requests

# catalog_page = requests.get(catalog_page_url)
catalog_page = requests.get(catalog_page_url_xcom)

print(catalog_page.status_code)

soup = BeautifulSoup(catalog_page.text, 'html.parser')

container_tag = "div"
container_attr = "class"

container_aval = "e1lmhh4u0 app-catalog-p8lfth e1loosed0"
container_aval_part = "app-catalog-"
dns_container_aval = "catalog-products view-simple"
dns_container_aval_part = "catalog-products"
xcom_container_aval = "catalog_items"
xcom_block_tag = "div"


counter = 0
# a = soup.find_all(attrs={container_attr: xcom_container_aval})

# for el in soup.find_all("div"):
# for el in a:
#     print(el)
#     counter+=1

# print(counter)
# container = soup.find_all("div", class_="catalog_items")[0]
container = soup.find_all(container_tag, attrs = {container_attr: xcom_container_aval})[0]

print(len(container))
# container_elems = container.find_all(container_tag)
# for elem in container.contents:
c_divs = []
for elem in container.children:
# for elem in container_elems:
    if elem.name == xcom_block_tag:
        # print(type(elem))
        print(elem.name)
        c_divs.append(elem)
        counter+=1
print(counter)
# for c_tag in soup.find_all(container_tag):
#     if c_tag
