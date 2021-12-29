from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup

import re

'''http://bs4ru.geekwriter.ru/bs4ru.html'''
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




find_char = 'Диагональ экрана (дюймы)' #' экрана (дюймы)'
alist = soup.find_all(re.compile("[a-zA-Z]"))#, string = find_char) #
#alist = soup.find_all("dt") #, string = find_char
#alist = soup.body.parents

#for el in alist:
#    print(el.string)
#print(alist)

find_item = ''
for el in alist:
    if el.string != None:
        #print(type(el.string))
        if find_char in el.string:
            #print([el])
            find_item = el

print(find_item.parent.parent)


'''
1 Найти на сайте тег по тексту (характеристика)
2 в этом теге найти

Найти слово - определить его адрес (htmk/div/p/слово)
выделить теги (htmk/div/p/)
проверить соседние теги на наличие текста (html/div/) - вытащить текст

'''
