from openpyxl import Workbook

def list_to_excel(py_list, excel_path):
    wb = Workbook()
    current_sheet = wb.active
    for el in py_list:
        current_sheet.append(el)
    wb.save(excel_path)

from typing import Dict
def read_excel(headers: Dict, False) -> str:
    return headers

a = read_excel({"1": "abc"})
print(a)
b = read_excel()
print(b)
