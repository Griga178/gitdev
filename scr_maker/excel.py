from openpyxl import load_workbook

def read_xlsx(file_name, sheet_name = False):
    wb = load_workbook(file_name, read_only = True, data_only = True)

    if sheet_name:
        active_sheet = wb[sheet_name]
    else:
        active_sheet = wb[0]

    list_links = []
    for row in active_sheet.rows:
        scr_num = str(row[0].value)
        link_val = str(row[1].value)
        list_links.append([scr_num, link_val])

    return list_links
