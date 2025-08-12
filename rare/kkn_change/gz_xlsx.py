from openpyxl import Workbook

import getpass

def make_excel(x_rows):
    user_name = getpass.getuser()

    file_path = f'C:/Users/{user_name}/Desktop/gz_test.xlsx'

    wb = Workbook()
    # sheet = wb.get_sheet_by_name('Sheet')
    wb.remove(wb['Sheet'])

    ws = wb.create_sheet('Аис ГЗ')


    first_row = [
        '№',    'Наименование ККН',
        None,    None,    None,    None,    None,    None,
        'Требования к значениям показателей',
        None,    None,    None,    None,    None,
        '*отображаются только те характеристики где проставлена галочка "Характеристика применятся" ',
        None,    None,    None,    None,
        'Средняя цена с НДС, руб. из реестра товаров (справочно)',
        'Номер электронной заявки',
        'Российский товар',
        'Тип характеристики'
    ]

    second_row = [
        None,
        'ID ККН',    'Название товара',    'ОКПД2',    'Детализация',
        'Единица измерения',    'Товарная часть',
        'Показатель (характеристика) товара',
        'Минимальное значение показателя и/или максимальное значение показателя',
        None,
        'Показатели (характеристики), для которых указаны варианты значений',
        'Показатели (характеристики) значения которых не могут изменяться',
        'Единица измерения характеристики',    'Категория',    'Актуальность',
        'КТРУ',
        'Согласован администратором ЦМЭЦ',    'Согласован администратором КГЗ',
        'Предельная цена, руб.',    None,    None,    None,    None
    ]

    t_row = [
        None, None, None, None, None, None, None, None,
        'Не менее', 'Не более', 'Справочник', None, 'Справочник'
    ]

    f_row = [1,2,3,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    ws.append(first_row)
    ws.append(second_row)
    ws.append(t_row)
    ws.append(f_row)
    for x_row in x_rows:
        ws.append(x_row)

    wb.save(file_path)
