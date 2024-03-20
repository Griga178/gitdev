'''
Выгрузка в excel
'''
from step_4 import *
# save_all_links() # step_1 - добавляем ссылки в БД
# parse_comp_id() # step_2 - скачивается id компании из карточки товара
# getOGRN() # step_3 - скачивается огрн по id из api ozon
egrul_parse() # step_4 - по огрн ищем инфу по компании на сайте egrul


def step_5():
    path_desktop = 'C:/Users/G.Tishchenko/Desktop/'

    excel_name_out = path_desktop + 'ozon_out_2.xlsx'

    wb = Workbook()
    active_sheet = wb.active

    data = db_session.query(Link).join(Company).filter(Link.company_id != None, Company.inn != None).all()

    print(len(data))

    def reform(row):
        # если ИП
        if row.company.short_name:
            name = row.company.short_name
        else:
            name = 'ИП ' + row.company.full_name
        cust_tuple = (
            row.excel_value,
            name,
            str(row.company.inn),
            # row.__dict__
            )
        return cust_tuple

    # print(reform(data[0]))

    for row in data:
        # print(reform(row))
        active_sheet.append(reform(row))

    wb.save(excel_name_out)

step_5()
