import sys
from my_mod import excel_to_list
if len(sys.argv) > 1:
    file_path = sys.argv[1:][0]
    # for file_path in sys.argv[1:]:
    #     print(file_path)


# ВЫГРУЖАЕМ ИЗ ФАЙЛА СПИСОК ИСПОЛЬЗОВАННЫХ ИНН
inn_list = excel_to_list(file_path, headers_names = ['ИНН поставщика', 'Источник ценовой информации'], headers = False, sheet_name = 'Реестр 1 кв 2023г')
print(len(inn_list))
inn_set = set()
for el in inn_list:
    print(el)
    if el[0][0] == "Э" or el[0][0] == "О":
        inn_set.add(el[1])
        # print(el)

# ВЫГРУЖАЕМ ИЗ SQL ДАННЫЕ ПО ИНН
for inn in inn_set:
    print(inn)
# ЕСЛИ НЕТ ДАННЫХ ПАРСИМ
input('input')
