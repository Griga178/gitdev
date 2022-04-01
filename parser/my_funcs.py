
import re

def define_main_page(link):
    '''
    Определение главной страницы из строки
    '''
    if type(link) == str:
        split_list = link.split("/")
        h_protocol = split_list[0]
        try:
            main_page = split_list[2]
        except:
            main_page = ''
        if 'http' or 'ftp' in h_protocol:
            return main_page
        else:
            print('ERROR: не похоже на ссылку')
            return False
    else:
        print('ERROR: ссылка не в формате строки')
        return False


def clean_number(str_text):
    ''' Выводит только числа из строк с помощью регулярок
        находит числа в которых "." или "," используется
        только для копеек'''
    result = re.findall(r'\d+\.?\,?', str_text)

    clear_number = ''.join(result)
    if ',' in clear_number:
        clear_number = clear_number.replace(',', '.')
    try:
        clear_number = float(clear_number)
        return clear_number
    except:
        print(f'Не преобразовать в число: {result, clear_number}')
        return False

link = 'https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-3101-chernyi-1001427/'

link = '''https://www.citilink.ru/product/karta-pamyati-microsdhc-uhs-i-kingston-canvselect-plus-32-gb-100-mb-s-1206983/
https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-110-chernyi-389726/
https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-3104-chernyi-1001429/
https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-108-chernyi-389721/
https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-3101-chernyi-1001427/
'''
# print(define_main_page(link))
# # #
# re_sult = re.findall(r'[\w:/.-]+', link)
#
# print(re_sult)



# def my_ret(fr, counter, all_amount):
#     print(fr, end = ' ')
#     return f'{counter}/{10}'
#
# counter = 0
# x = 10
# for el in range(x):
#     counter += 1
#     print(my_ret('hello', counter, x))
