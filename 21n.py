'''
создание таблицы уникальных поставщиков из excel
'''
import openpyxl

excel_file_name = 'C:/Users/G.Tishchenko/Desktop/reestr 2022 (текущ).xlsx'

sheet_name = 'Поставщики'

def read_excel():
    'Создаем список с [ИНН, Наименование поставщика, Сайт]'
    #work_list = []
    companies_dict = {}
    wb = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = wb[sheet_name]
    counter = 0
    for row in active_sheet.rows:
        main_page_temp_set = set()
        # чтение ячеейк в строках и добавление в "список строки"
        inn_value = str(row[0].value)
        name_value = str(row[1].value)
        link_value = str(row[2].value)
        # если в ячейке больше 2 ссылок с '\n' берем только первую
        try:
            if '\n' in link_value:
                link_value = link_value.split("\n")[0] # убираем места с двумя ссылками
            # названия главной страницы
            main_page = (link_value.split("/")[2])
        except:
            print(counter, 'trouble with main_page')
            pass

        main_page_temp_set.add(main_page)

        if main_page == 'zakupki.gov.ru':
            pass
        else:
            # Проверка на совпадение имени и ИНН
            if inn_value in companies_dict:
                if name_value == companies_dict[inn_value][0]:
                    companies_dict[inn_value][1].add(main_page)
                else:
                    print(counter, name_value, companies_dict[inn_value][0])
            else:
                companies_dict |= {inn_value: [name_value, main_page_temp_set]}
        counter += 1


    #print(len(companies_dict))

    return companies_dict


def write_to_csv():
    write_dict = read_excel()
    csv_new_name = 'C:/Users/G.Tishchenko/Desktop/Поставщики2.csv'
    with open(csv_new_name, 'w') as file:
        for line in write_dict:
            file.write(f'{line};{write_dict[line][0]}') #;{write_dict[line][1]}\n
            for el in write_dict[line][1]:
                file.write(f';{el}')
            else:
                file.write(f'\n')
write_to_csv()
