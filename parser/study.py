from my_parser import product_block

title_a = product_block.title
name_block = product_block.name
parnt_name = product_block.parent.name

# Вызов по тегу
something = product_block.div
# значение атрибута
#something['class']
something_else = product_block.contents[0]

# for el in something_else:
#     #print(el.name)
#     # Получение всех аттрибутов тега
#     #print(el.attrs)
#     # Обращение к определенному атрибуту
#     #print(el['class'])
#     # Отображение всех строк в теге
#     if 'ProductHeader__price-block' in el['class']:
#          # for string in el.stripped_strings:
#          #     print(string)
#         a = 0
#         for string in el.descendants:
#             a+=1
#             print(a, string.name)
#             try:
#                 if string['class']:
#                     print(string['class'])
#             except:
#                 print(string.string)
        # print('DA')
        # a = 0
        # for tag_class in el:
        #     a+=1
        #     print(a, tag_class.name, tag_class['class'])
        #     for jel in tag_class:
        #         print(jel.name, type(jel))
tags_dict = {'www.citilink.ru':
    {'price_block': ['div', 'class', 'ProductHeader__price-block'],
    'old_price_path': [['div', 'class', 'ProductHeader__old-price'],
                        ['div', 'class', 'ProductHeader__old-price'],
                        ['span', 'class', 'ProductHeader__old-price']
                        ]
    }
}
print(product_block.find('span', 'ProductHeader__price-default_current-price').string)

full_xpath = '/html/body/div[2]/div[2]/main/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/div[5]/div[1]/div[2]/div/span/span[1]'


# https://ru-qt4.livejournal.com/3827.html
