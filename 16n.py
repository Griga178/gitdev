import pickle
import openpyxl
'''
РАСПАКОВКА PICLE ФАЙЛА В EXCEL
'''
pkl_path = 'C:/Users/G.Tishchenko/Desktop/11_part_v2/price.pkl'
excel_path = 'C:/Users/G.Tishchenko/Desktop/11_part_v2/prices2.xlsx'

with open(pkl_path, 'rb') as f:
    dub_list = pickle.load(f)

wb = openpyxl.Workbook()
current_sheet = wb.active

for el in dub_list:
    current_sheet.append(el)

wb.save(excel_path)
