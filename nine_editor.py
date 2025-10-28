def edit_row_v2(exel_row, prev_row = False):
    excel_row = {}
    # print(exel_row)
    # Обработка строк
    if prev_row:
        excel_row['kkn_name'] = exel_row[0] if exel_row[0] else prev_row['kkn_name']
    else:
        excel_row['kkn_name'] = exel_row[0]

    excel_row['kkn_name'] = exel_row[0]
    excel_row['source'] = exel_row[1]
    excel_row['company_inn'] = exel_row[2]
    excel_row['company_name'] = exel_row[3]
    excel_row['screen_number'] = exel_row[4]
    excel_row['price'] = exel_row[5]

    if excel_row['source'] and excel_row['price']:
        if excel_row['source'][0].upper() == 'О':
            excel_row['source_type'] = "Ответ на запрос"
            spl_row = excel_row['source'].split("-")
            excel_row['source_type_number'] = spl_row[1][:-3]
        elif excel_row['source'][0].upper() == 'Э':
            excel_row['source_type'] = "Экранная копия"
            spl_row = excel_row['source'].split("-")
            excel_row['source_type_number'] = spl_row[1][:-3]
        elif len(excel_row['source']) == 33:
            excel_row['source_type'] = "Контракт"
            spl_row = excel_row['source'].split(" ")
            excel_row['source_type_number'] = spl_row[0]
        else:
            excel_row['source_type'] = "Пусто"
            excel_row['source_type_number'] = 0
    else:
        excel_row['source_type'] = "Пусто"
        excel_row['source_type_number'] = 0

    return excel_row

def combine_info_v2(ex_list):
    information = {
        'Экранные копии': {},
        'Ответы на запрос': {}
    }
    ekranki = []
    otveti = []
    prev_row = False
    for ex_row in ex_list:
        row = edit_row_v2(ex_row, prev_row)
        prev_row = row

        # Делим по "Источник ценовой информации"
        if row['source_type'] == "Экранная копия":
            ekranki.append(row)
        elif row['source_type'] == "Ответ на запрос":
            otveti.append(row)

    for ekr in ekranki:
        if ekr['company_inn'] in information['Экранные копии']:
            information['Экранные копии'][ekr['company_inn']]['screens'].append(func4(ekr))
        else:
            information['Экранные копии'][ekr['company_inn']] = func3(ekr)

    for ekr in otveti:
        if ekr['company_inn'] in information['Ответы на запрос']:
            information['Ответы на запрос'][ekr['company_inn']]['screens'].append(func4(ekr))
        else:
            information['Ответы на запрос'][ekr['company_inn']] = func3(ekr)

    return information

def func3(row):
    ld = {
        'screens': [{
                "name": row['screen_number'],
                'kkn_name': row['kkn_name']}],
        'number': row['source_type_number'],
        'company_name': row['company_name'],
        'source': row['source'],
    }
    return ld
def func4(row):
    ld = {
        "name": row['screen_number'],
        'kkn_name': row['kkn_name']
    }
    return ld

'''
    FROM EXCEL
        [
            [
            'Наименование ККН',
            'Источник ценовой информации',
            'ИНН поставщика',
            'Наименование поставщика',
            'Номер скрина',
            'Новая цена'
            ]
        ]
    UPDATE INFO
        {
        'Экранные копии': {
            '<Наименование поставщика>': {
                    'screens': [
                        {
                        'name': '1',
                        'kkn_name': 'string',
                         }
                        ],
                    'number': 'Источник ценовой информации',
                    'company_name': 'Наименование поставщика',
                }, ...

            },
        'Ответы на запрос': {
            'как и в экранках'
        }
        }
'''
