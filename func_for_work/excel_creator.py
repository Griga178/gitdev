import openpyxl

desktop_path = 'C:/Users/G.Tishchenko/Desktop/'

excel_links_table = 'Work_links_test.xlsx'

excel_companies_info = 'Companies_info_test.xlsx'



def create_new_work_table():
    file_path = desktop_path + excel_links_table

    wb = openpyxl.Workbook()

    current_sheet = wb.active

    current_sheet.title = "work_links"

    current_sheet.cell(row = 1, column = 1).value = "Company INN"
    current_sheet.column_dimensions['A'].width = 13
    current_sheet.cell(row = 1, column = 2).value = "Link/screen number"
    current_sheet.column_dimensions['B'].width = 19
    current_sheet.cell(row = 1, column = 3).value = "Link"
    current_sheet.column_dimensions['C'].width = 13
    current_sheet.cell(row = 1, column = 4).value = "Main page"
    current_sheet.column_dimensions['D'].width = 13
    current_sheet.cell(row = 1, column = 5).value = "Price"
    current_sheet.column_dimensions['E'].width = 13
    current_sheet.cell(row = 1, column = 6).value = "Name"
    current_sheet.column_dimensions['F'].width = 13
    current_sheet.cell(row = 1, column = 7).value = "Parsed date"
    current_sheet.column_dimensions['G'].width = 13
    current_sheet.cell(row = 1, column = 7).value = "Status"
    current_sheet.column_dimensions['H'].width = 13
    current_sheet.cell(row = 1, column = 7).value = "Part"
    current_sheet.column_dimensions['I'].width = 13

    wb.save(file_path)

def create_companies_file():
    file_path = desktop_path + excel_companies_info

    wb = openpyxl.Workbook()

    current_sheet = wb.active

    current_sheet.title = "companies_info"

    current_sheet_2 = wb.active
    current_sheet_2.title = "site_settings"

    wb.save(file_path)

def update_work_table(excel_info):
    pass


def update_companies_file():
    pass

create_companies_file()
# create_new_work_table()
