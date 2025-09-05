"""
    создание таблицы для вывода в консоль (в markdown)
    заполнить:
    headers     - заголовки
    width       - ширина каждого столбца
    в li[2:]    - содержимое строк
"""
headers = ['Поле','Тип','Описание']
width = (13, 13, 40)
# КОЛИЧЕСТВО СТОЛБЦОВ
clmn = len(headers)
# ШИРИНА СТОЛБЦОВ
# width = max(len(item) for item in headers) + 2

sep_r = []
for i in range(clmn):
    sep_r.append('-' * width[i])
li = [
    headers,
    sep_r,
    ['id','Integer PK','-'],
    ['name','String','"example.com"'],
    ['settings','String','настройки для парсинга в формате json'],

]

rows = []
for li_row in li:
    row = '|'
    clmn_idx = 0
    for el in li_row:
        row += el.ljust(width[clmn_idx]) + '|'
        clmn_idx += 1

    rows.append(row)

for r in rows:
    print(r)
