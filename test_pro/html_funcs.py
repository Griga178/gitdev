import requests
import bs4
from bs4 import BeautifulSoup



''' http://bs4ru.geekwriter.ru/bs4ru.html
    https://tproger.ru/translations/regular-expression-python/ '''

uri = 'https://www.lg.com/ru/monitors/lg-27MP77HM-P'

''' Текст для поиска '''
product_group = 'Мониторы '
product_name = 'IPS монитор LG серии MP77'
article_number = '27MP77HM-P'
find_char = 'Диагональ экрана' #' экрана (дюймы)'

uri_page = requests.get(uri)
soup = BeautifulSoup(uri_page.text, 'html.parser')

#print(soup.prettify())
#print(soup.title)
#print(soup.title.name)
#print(soup.title.parent.name) #
#print(soup.p)
#print(soup.find_all('p'))
#print(uri_page.text)

''' Список всех тегов (+ RegEx) - в виде экземпляров класса '''
alist = soup.find_all(re.compile("[\w]+")) # '\' и любой англ.символ

''' Поиск текста среди всех тегов '''
for el in alist:
    if el.string != None:
        if find_char in el.string:
            find_item = el

def clean_text(str_text):
    ''' выделение символов и цифр в строке с помощью регулярок '''
    #result = re.findall(r'[\wа-яА-ЯёЁ\d() .!,?:;-]+', str_text)
    result = re.findall(r'[^\n\t]+', str_text)
    clear_text = ''.join(result)
    return clear_text

''' 1 случай:
    Имя - значение находятся в 1-ом теге = "Группа" (<tr> <p>"Name"</p> <p>"Val"</p> </tr>) '''

def first_case(val_tag):
    # Поиск всех тегов в Группе
    parent_tag_list = val_tag.parent
    char_name = clean_text(val_tag.string)
    value = None
    for el in parent_tag_list:
        if type(el) == bs4.element.Tag and el.string != val_tag.string:
            try:
                value = clean_text(el.string)
            except:
                value = 'Error'
    print([char_name], '-', [value])

new_list = soup.find_all(find_item.name)

#for el in new_list:
#    first_case(el)

''' Сохранение настроек сайта для дальнейшего парсинга всех товаров:
        Как найти (имея пример):
            Артикул = ссылкка - Есть
            Категорию товара
            Характеристики товара - Есть
            '''
# Поиск Артикула article_number
new_soup_l = soup.find_all('nav', {'class':'breadcrumb'})[0]
print([el for el in new_soup_l.text.split('\n') if el][-1])
print([el for el in new_soup_l.text.split('\n') if el][-2])
# Поиск Категории product_group

'''
    Задачи:
        найти все теги с текстом

'''
