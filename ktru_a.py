"""
0. формируем excel с неактуальными КТРУ (updated_ktru_excel_path)
1. получаем список номеров ктру -> ktru_list = [str, ...]

2. парсим все КТРУ

3. выгружаем из справочника (reestr_kkn_excel_path) ККН где используется эти ктру

4. сравниваем характеристики ККН с хар-ми КТРУ parse_kkn_excel -> kkn_full_list


days_expiry = 1 - указать для исключения повторных запросов

"""

from zakupki import Controller
from excel_funcs import get_reestr
# from excel_funcs.check_kkn import check_reestr
# from excel_funcs.write_kkn import write_worked_list_to_excel
from excel_funcs.write_kkn_with_ktru import write_checked_worked_list_to_excel
from excel_funcs.compare_ktru import compare_ktru_chars
from excel_funcs.check_kkn_vs_checked_ktru import check_reestr_vs_checked_ktru

import openpyxl
import re

def get_ktru_list(excel_path):
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    sheet = wb.worksheets[0]
    ktru_list = []

    # валидация
    pattern = r'\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{8}'

    # пропускаем заголовок, начинаем со второй строки
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        value = row[0]
        if value is not None:
            match_inside = re.search(pattern, value)

            if match_inside:
                ktru_list.append(str(match_inside.group()))

    return ktru_list


updated_ktru_excel_path = 'C:/Users/G.Tishchenko/Downloads/ктру0925.xlsx'
# reestr_kkn_excel_path = 'C:/Users/G.Tishchenko/Desktop/94-ККН ЦМЭЦ на 01.07.2025 (8791).xlsx'
reestr_kkn_excel_path = 'Z:/Официальная публикация/Справочник ККН/97-ККН ЦМЭЦ на 01.10.2025 (8866).xlsx'

# читаем файл с неактуальными КТРУ
ktru_set = set(get_ktru_list(updated_ktru_excel_path))
ktru_set = sorted(list(ktru_set))
# ktru_set = ["01.13.19.000-00000001"]
# Подгружаем инфу по этим КТРУ (актуальные версии)
uploaded_ktru = []
ktru_len = len(ktru_set)
ktru_idx = 0
days_expiry = 1 # срок годности скачанных ктру (если скачаны раньше - качаем заново)
import time
for valid_ktru_number in ktru_set:
    ktru_idx += 1
    msg = f'{ktru_len}/{ktru_idx}'.center(10)
    print(msg)
    # time.sleep(0.5)
    result = Controller.fetch_parse_and_store_ktru(valid_ktru_number, days_expiry=days_expiry)

    if isinstance(result.get('version'), int) and result['version'] > 1:
        version_0 = result['version'] - 1
    else:
        version_0 = None

    result_0 = Controller.fetch_parse_and_store_ktru(valid_ktru_number, version_0, days_expiry=days_expiry)

    checked_ktru = compare_ktru_chars(result, result_0)
    uploaded_ktru.append(checked_ktru)



print("\nuploaded", len(uploaded_ktru))

# читем файл Справочник ККН
print("Чтение справочника ККН...")
reestr_kkn = get_reestr.parse_kkn_excel(reestr_kkn_excel_path)

print("Сравнение ККН и КТРУ...")
checked_reestr_kkn = check_reestr_vs_checked_ktru(ktru_set, reestr_kkn, uploaded_ktru)

print("Запись в EXCEL...")
write_checked_worked_list_to_excel(checked_reestr_kkn, updated_ktru_excel_path)


'''
NEXT TO DO:
- понять что ккн надо менять
- на втором листе оставить ККН для изменения

имена ключей ktru_dict и типы значений [
    ktru_id:int,
    name:str,
    number:str,
    version:int,
    chars_count:int,
    chars:list[ktru_char, ...]]
имена ключей chars и типы значений [
    id:int,
    ktruVersionId:int,
    name:str,
    unit:str,
    isRequired:bool,
    values:list[str,...]]

checked_reestr_kkn[0] ={
    'num': int, 'kkn_name': str, 'kkn_okpd_2': str, 'kkn_det_num': str, 'kkn_unit': str,
    'category_name': str, 'ktru_number': str, 'kkn_number': str, 'product_part': str,
    'upt_date': datetime, 'is_russian': bool, 'rrrp_number': str,
    'kkn_chars': [
        {
        'name': str, 'unit': str, 'value_is_range': bool, 'value_range': (str, str),
        'values': [str,], 'belongs_to_kkn': bool,
        'ktru_data':
            {
            'ktru_char': bool, 'all_right': bool, 'errors': [],
            'ktru_char_origin':
                {
                'id': 1254, 'ktruVersionId': 39, 'name': str,
                'values': list[str,...], 'unit': str, 'isRequired': bool,
                'version_data':
                    {
                    'isDelete': bool, 'isNew': bool, 'isChanged': bool,
                    'new_val': list[str,...], 'delete_val': list[str,...]
                    }
                }
            }
        },...
    ],
}
'''
