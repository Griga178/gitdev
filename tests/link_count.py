'''
Цель:
Перед парсингом узнать сколько ссылок мы (не)сможем пропарсить и добавить
настройки для неизвестных ссылок
Здесь 4 функции:
1 создание словаря из доменов и их количества (dict_of_links_from_excel)
2 заполнение списка известных ссылок (my_known_domain)
3 выбирает из всех доменов неизвестные, делит на: частые/редкие (unknown_domains)
4 объединяет старые домены с новыми
3-4 - записывают инфу в файлы .csv
* прога, которая будет считать скорость парсинга, скриншотов
** добавить: Всего ссылок в файле ( шт.) + известные / неизвестные
'''
import pandas
from collections import Counter

#import time
#start_time = time.time()

excel_name = '../devfiles/reestr 4.xlsx' #'files/Реесть 4кв.xlsx'
sheets_name = 'RT new' #'RT new'
column_links = 'Ссылка'

txt_file_name = 'settings/alles_links.csv'
beauty_file_name = 'settings/my_beauty_links.csv'
selenium_file_name = 'settings/my_selenium_links.csv'
unknown_domains_file_name = 'settings/unknown_domains.csv'
unknown_important_domains_file_name = 'settings/unknown_important_domains.csv'

def dict_of_links_from_excel(excel_name, sheets_name, column_links):
    '''
    Экспорт ссылок из excel в словарь
        создает отсортированый по убыванию словарь {}:
            домен - количество ссылок на него
    '''
    data = pandas.read_excel(excel_name, sheet_name = sheets_name, usecols =[column_links])
    list_links = data[column_links].tolist()
    # Выделяем домен из ссылки, заносим в список
    list_domain = []
    for link in list_links:
        link = str(link)
        try:
            main_page = link.split("/")[2]
        except:
            pass
        list_domain.append(main_page)
    # создаем словарь: домен - количество (dns.ru:100)
    dict_domain = {domain : list_domain.count(domain) for domain in list_domain}
    # сортируем по убыванию
    sorted_dict = {}
    sorted_list = sorted(dict_domain, key = dict_domain.get, reverse = True)
    for domain in sorted_list:
        sorted_dict[domain] = dict_domain[domain]
    return sorted_dict

def my_known_domain():
    '''
    Возвращает список изученных доменов,
    для которых есть настройки парсинга в my_beauty_links/my_selenium_links
    нужен для подсчета неизученных доменов
    '''
    list_known_domain = []
    with open(beauty_file_name, 'r') as file:
        for line in file:
            domain = line.split(';')[0]
            list_known_domain.append(domain)
    with open(selenium_file_name, 'r') as file:
        for line in file:
            domain = line.split(';')[0]
            list_known_domain.append(domain)
    return list_known_domain

def unknown_domains():
    '''
    создает множество (set) неизученных доменов
    записывает это в файлы:
        *unknown_domains_file_name - все неизвестные домены
        *unknown_important_domains_file_name - неизвестные домены, которые
        встретились больше 10 раз
    '''
    sorted_dict = dict_of_links_from_excel(excel_name, sheets_name, column_links)
    set_all_domains = set()
    set_important_domains = set()
    try:
        with open(unknown_domains_file_name, 'r') as file:
            # Заполняем множество неизвестных доменов (старых)
            for el in file:
                set_all_domains.add(el.replace("\n", ""))
    except:
        print(f'Создан новый: {unknown_domains_file_name}')
    # Заполняем множество неизвестных доменов (новых)
    for el in sorted_dict:
        set_all_domains.add(el)
        if sorted_dict[el] > 10:
            set_important_domains.add(el)
    # Открываем множество известных доменов
    set_known_domains = set(my_known_domain())
    # Оставляем только неизвестные домены
    set_unknown_domains = set_all_domains - set_known_domains
    set_unknown_important_domains = set_important_domains - set_known_domains
    print(f'Неизученных доменов: {len(set_unknown_domains)} шт.')
    print(f'Неизученных важных доменов: {len(set_unknown_important_domains)} шт.')
    with open(unknown_domains_file_name, 'w') as file:
        for el in set_unknown_domains:
            file.write(f'{el}\n')
    with open(unknown_important_domains_file_name, 'w') as file:
        for el in set_unknown_important_domains:
            file.write(f'{el}\n')

def count_all_domains():
    '''
    функция создает/добавляет к старому файл с доменами и их количеством
    в текстовый файл
    '''
    sorted_dict = dict_of_links_from_excel(excel_name, sheets_name, column_links)
    try:
        with open(txt_file_name, 'r') as file:
            line = file.readline().split(':')[:-1] # список уже изученных файлов excel
            new_file_name = excel_name.split('/')[-1]
            if new_file_name in line:
                print(f'Файл: "{new_file_name}" уже был добавлен' )
                #return
            line.append(new_file_name) # добавление имени нового файла line.append('Реесть 4кв.xlsx')
            print(f'Изученные файлы excel: {line}')
            first_row = ':'.join(line)
            print(first_row)
            current_dict_domains = {}
            for line in file:
                f_key, f_value = line.split(':')[0], int(line.split(':')[1])
                current_dict_domains.update({f_key: f_value})
    except:
        current_dict_domains = {}
        first_row = excel_name.split('/')[-1]
    tuple_current_new_dict = (current_dict_domains, sorted_dict)
    updated_domain_dict = Counter()
    for domain in tuple_current_new_dict:
        updated_domain_dict.update(domain)
    with open(txt_file_name, 'w') as file:
        file.write(f'{first_row}:\n')
        for key in updated_domain_dict:
            file.write(f"{key}:{updated_domain_dict[key]}:\n")

# надо запустить эти две функции:
count_all_domains()
unknown_domains()
