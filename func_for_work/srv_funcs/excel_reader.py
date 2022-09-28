import openpyxl

# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/For_sed An.xlsx'

def open_excel(excel_file_name, sheet_number = 0):
    """возвращает генератор инф-и из excel """
    work_book = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = work_book.worksheets[sheet_number]
    rows_generator = active_sheet.iter_rows(min_row = 2)
    return rows_generator

def get_excel_rows(excel_file_name):
    return_list = []

    ab = open_excel(excel_file_name)

    for excel_row in ab:
        company_name =  excel_row[0].value.strip()
        company_type_number =  excel_row[1].value
        company_split = company_type_number.split(' ')

        if len(company_split) == 6:
            company_type = ' '. join(company_split[0:2])
        else:
            company_type = ' '. join(company_split[0:3])

        company_number = company_split[-1]

        return_list.append([company_type, company_number, company_name])

    return return_list
