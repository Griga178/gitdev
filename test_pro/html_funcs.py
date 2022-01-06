import requests
from bs4 import BeautifulSoup

import re

''' http://bs4ru.geekwriter.ru/bs4ru.html
    https://tproger.ru/translations/regular-expression-python/ '''

uri = 'https://www.lg.com/ru/monitors/lg-27MP77HM-P'


uri_page = requests.get(uri)
soup = BeautifulSoup(uri_page.text, 'html.parser')

#print(soup.prettify())
#print(soup.title)
#print(soup.title.name)
#print(soup.title.parent.name) #
#print(soup.p)
#print(soup.find_all('p'))
#print(uri_page.text)



''' Текст для поиска '''
find_char = 'Диагональ экрана (дюймы)' #' экрана (дюймы)'

''' Список всех тегов (+ RegEx) - в виде экземпляров класса '''
alist = soup.find_all(re.compile("[\w]+"))

''' Поиск текста среди всех тегов
    нужен вариант с множеством найденных текстов '''
for el in alist:
    if el.string != None:
        if find_char in el.string:
            find_item = el

#print(find_item.parent.parent)

def clean_text(str_text):
    ''' выделение символов и цифр в строке с помощью регулярок '''
    #result = re.findall(r'[\wа-яА-ЯёЁ\d() .!,?:;-]+', str_text)
    result = re.findall(r'[^\n\t]+', str_text)
    clear_text = ''.join(result)
    return clear_text




''' Нашли название характеристики - теперь ищем ее значение '''

# имя характеристики и значение находятся в своих тегах
# и объединены общим тегом (<tr><p>Name</p><p>Val</p></tr>)

find_val = find_item.next_sibling
clear_val = clean_text(find_val.string)
c = 0
print(c, find_item)
while len(clear_val) >= 0:
    c += 1
    print(c, find_val)

    find_val = find_val.next_sibling

    clear_val = clean_text(find_val.string)
    print([clear_val])
else:
    print('yeah')
    print([clear_val])


#print([find_item.next_sibling.next_sibling.string]) #.string

#print(clean_text(find_item.next_sibling.next_sibling.string))
'''
1 Найти на сайте тег по тексту (характеристика)
2 в этом теге найти

Найти слово - определить его адрес (htmk/div/p/слово)
выделить теги (htmk/div/p/)
проверить соседние теги на наличие текста (html/div/) - вытащить текст

'''
