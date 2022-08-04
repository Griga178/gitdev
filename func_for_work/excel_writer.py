import openpyxl

def write_links_data(links_data, excel_file_name):

    links_table_file = openpyxl.load_workbook(excel_file_name)

    current_sheet = links_table_file['work_links']

    for row in links_data:
        current_sheet.append(row)

    links_table_file.save(excel_file_name)

desktop_path = 'C:/Users/G.Tishchenko/Desktop/'
main_folder = desktop_path + 'main/'
comp_info_table = main_folder + 'companies_info.xlsx'
# links_table_file = main_folder + 'links_table.xlsx'
#
# my_data = [['inn1', 'main_page', 'links1', 'number']]

# write_links_data(my_data, links_table_file)

def write_comp_info(comp_data, excel_file_name):

    comp_info_file = openpyxl.load_workbook(excel_file_name)

    curren_sheet = comp_info_file['companies_info']

    out_put = [(str(cel_val.value) + "s") for cel_val in curren_sheet["A"]]

    print(out_put)

    comp_info_file.save(excel_file_name)

compi_data = [1,2,3]
# write_comp_info(compi_data, comp_info_table)
