def edit_row_v2(exel_row, prev_row = False):
    excel_row = {}
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

    if source[0].upper() == 'О':
        excel_row['source_type'] = "Ответ на запрос"
        spl_row = source.split("-")
        excel_row['source_type_number'] = spl_row[1][:-3]
    elif source[0].upper() == 'Э':
        excel_row['source_type'] = "Экранная копия"
        spl_row = source.split("-")
        excel_row['source_type_number'] = spl_row[1][:-3]
    elif len(source) == 33:
        excel_row['source_type'] = "Контракт"
        spl_row = source.split(" ")
        excel_row['source_type_number'] = spl_row[0]

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
        row = edit_row(ex_row, prev_row)
        prev_row = row

        # Делим по "Источник ценовой информации"
        if ex_row['source_type'] == "Экранная копия":
            ekranki.append(ex_row)
        elif row['source_type'] == "Ответ на запрос":
            otveti.append(ex_row)

    for ekr in ekranki:
        if ekr['company_inn'] in information['Экранные копии']:
            pass
        else:
            information['Экранные копии'][ekr['company_inn']] = 

def combine_info_edition(row):
