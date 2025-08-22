
import openpyxl
from typing import List, Dict, Any, Tuple

def parse_kkn_excel(path: str) -> List[Dict[str, Any]]:
    """
    List = [kkn_dict]
    имена ключей kkn_dict и типы значений [
        num:int
        kkn_name:str,
        kkn_okpd_2:str,
        kkn_det_num:str,
        kkn_unit:str,
        kkn_chars:list[kkn_char,...],
        category_name:str,
        ktru_number:str,
        product_part:str,
        upt_date:str,
        is_russian: str,
        rrrp_number: str,
        ]
    имена ключей kkn_char и типы значений [
        name:str,
        unit:str,
        value_is_range:bool
        value_range:tuple[float,float] # min, max
        values:list[str,...]
    ]
    """
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active

    products = []
    current_product = None

    # Индексы столбцов (1-based)
    # исходя из описания:
    # 1 номер (int)
    # 2 Наименование ККН (str)
    # 3 окпд2 (str)
    # 4 детализация (str)
    # 5 ед. изм (str)
    # 6 наименование характеристики (str)
    # 7 значение мин (float)
    # 8 значение макс (float)
    # 9 несколько значений на выбор (str(";"))
    # 10 одно значение (str)
    # 11 ед. изм (str)
    # 12 Наименование Категории (str)
    # 13 Код ктру (str)
    # 14 код ккн (str)
    # 15 часть (str)
    # 16 дата (str)
    # 17 страна Россия (bool)
    # 18 номер РРРП (str)

    for row in ws.iter_rows(min_row=5):  # С 5-й строки (1-й = 1)
        num_cell = row[0].value  # столбец 1
        if num_cell is not None:
            # Новый товар, если в 1-й ячейке что-то есть
            if current_product:
                products.append(current_product)

            # Разбор основных данных товара
            is_russian_val = row[16].value
            # Преобразование в bool — если в ячейке True или что-то, трактуем True, иначе False
            is_russian = bool(is_russian_val) if is_russian_val is not None else False

            current_product = {
                "num": int(row[0].value),
                "kkn_name": str(row[1].value) if row[1].value is not None else "",
                "kkn_okpd_2": str(row[2].value) if row[2].value is not None else "",
                "kkn_det_num": str(row[3].value) if row[3].value is not None else "",
                "kkn_unit": str(row[4].value) if row[4].value is not None else "",
                "kkn_chars": [],
                "category_name": str(row[11].value) if row[11].value is not None else "",
                "ktru_number": str(row[12].value) if row[12].value is not None else "",
                "kkn_number": str(row[13].value) if row[13].value is not None else "",
                "product_part": str(row[14].value) if row[14].value is not None else "",

                "is_russian": is_russian,
                "rrrp_number": str(row[17].value) if row[17].value is not None else "",
            }
            current_product["upt_date"] = row[15].value if row[15].value is not None else None

        # Добавляем характеристику к текущему товару
        if current_product is None:
            # Строка до первого товара — пропускаем
            continue

        char_name = row[5].value
        if char_name is None:
            continue  # Пустая характеристика — пропускаем

        # Значения характеристики
        # вариант 1: есть min и max (7,8)
        val_min = row[6].value
        val_max = row[7].value
        # вариант 2: несколько значений (9)
        mult_values_str = row[8].value
        # вариант 3: одно значение (10)
        one_value_str = row[9].value

        value_is_range = False
        value_range: Tuple[float, float] = (0.0, 0.0)
        values: List[str] = []

        if val_min not in (None, "") or val_max not in (None, ""):
            try:
                min_f = val_min if val_min not in (None, "") else None
                max_f = val_max if val_max not in (None, "") else None
                # добавляем как строки
                # min_f = float(min_f.replace(',','.'))
                # max_f = float(max_f.replace(',','.'))
                value_is_range = True
                value_range = (min_f, max_f)
                values = []
            except (ValueError, TypeError):
                value_is_range = False
                value_range = (0.0, 0.0)
                values = []
        elif mult_values_str not in (None, ""):
            values = [v.strip() for v in mult_values_str.split(";") if v.strip()]
            value_is_range = False
            value_range = (0.0, 0.0)
        elif one_value_str not in (None, ""):
            values = [str(one_value_str).strip()]
            value_is_range = False
            value_range = (0.0, 0.0)
        else:
            value_is_range = False
            value_range = (0.0, 0.0)
            values = []

        unit = str(row[10].value) if row[10].value is not None else ""

        char_dict = {
            "name": str(char_name),
            "unit": unit,
            "value_is_range": value_is_range,
            "value_range": value_range,
            "values": values
        }
        current_product["kkn_chars"].append(char_dict)

    # Добавить последний товар в список
    if current_product:
        products.append(current_product)

    return products
