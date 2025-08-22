"""
сравнение характеристик ККН с КТРУ новой и предыдущей версией
"""

from typing import List, Dict, Tuple, Any

def validate_values(values):
    validate_list = []
    for val in values:
        if val == '0':
            continue
        if val == 'Не установлено':
            continue
        val = val.replace(' ', '')
        val = val.replace(',', '.')

        val = val.replace('.0', '')
        val = val.replace('х', 'x')
        val = val.replace(' x ', 'x')

        validate_list.append(val)
    return validate_list

def get_ktry_by_num(ktru_number: str, uploaded_ktru: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Вспомогательная функция для поиска КТРУ по номеру.
    Возвращает dict с найденной записью или пустой dict.
    """
    for ktru in uploaded_ktru:
        if ktru.get('number') == ktru_number:
            # Копируем, чтобы не изменять оригинал
            return {
                **ktru,
                'chars': ktru.get('chars', []).copy()
            }
    return {}

def find_char_by_name(chars: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
    """
    Поиск характеристики по имени в списке chars.
    Возвращает найденный dict или None.
    """
    for char in chars:
        if char.get('name') == name:
            return char
    return None

def check_reestr_vs_checked_ktru(ktru_set: Tuple[str, ...],
                 reestr_kkn: List[Dict[str, Any]],
                 uploaded_ktru: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Проверка реестра ККН по обновлённым КТРУ

    Аргументы:
    - ktru_set: Кортеж номеров КТРУ (tuple[str,...])
    - reestr_kkn: Список словарей с полной информацией ККН (list[dict])
    - uploaded_ktru: Список обновленных КТРУ (list[dict])

    Возвращает:
    - worked_list: список ККН с обновлённой информацией по характеристикам,
      где каждое 'kkn_char' содержит ключ 'ktru_data' со статусом проверки.
    """
    worked_list = []

    for kkn in reestr_kkn:
        kkn_number = kkn.get('ktru_number')
        if kkn_number not in ktru_set:
            continue

        current_ktru_copy = get_ktry_by_num(kkn_number, uploaded_ktru)
        # Работать с копией chars, чтобы можно было удалять совпавшие
        current_ktru_chars = current_ktru_copy.get('chars', [])
        # Чтобы быстро находить по имени KTRU char, лучше сделать индекс словарём:
        ktru_chars_dict = {char['name']: char for char in current_ktru_chars}

        kkn_chars = kkn.get('kkn_chars', [])

        # Перебираем характеристики ККН
        for kkn_char in kkn_chars:
            kkn_char_name = kkn_char.get('name')
            ktru_char = ktru_chars_dict.pop(kkn_char_name, None)  # Удаляем из словаря, если нашли

            if ktru_char:
                # Сравниваем значения
                kkn_values = set(validate_values(kkn_char.get('values', [])))
                ktru_values = set(validate_values(ktru_char.get('values', [])))
                # print([repr(i) for i in kkn_values])
                # print([repr(i) for i in ktru_values])
                missing_values = kkn_values - ktru_values  # значения из ККН, которых нет в КТРУ

                all_right = len(missing_values) == 0
                errors = list(missing_values)
                kkn_char['belongs_to_kkn'] = True
                kkn_char['ktru_data'] = {
                    'ktru_char': True,
                    'all_right': all_right,
                    'errors': errors,
                    # 'is_required': ktru_char.get('isRequired', None),
                    'ktru_char_origin': ktru_char.copy(),
                }
            else:
                # Нет характеристики в КТРУ, ставим флаг False
                isForbidden = current_ktru_copy.get('ownCharsIsForbidden')
                kkn_char['belongs_to_kkn'] = True
                kkn_char['ktru_data'] = {
                    'ktru_char': False,
                    'all_right': True if not isForbidden else False,
                    'errors': [],
                    # 'is_required': None,
                    'ktru_char_origin': {},
                }

        # Остались характеристики в current_ktru_chars, которые не совпали с ККН

        for char in ktru_chars_dict.values():
            char['belongs_to_kkn'] = False
            char_values = char.get('values', [])
            char['ktru_data'] = {
                'ktru_char': True,
                'all_right': False,
                'errors': char_values,
                # 'is_required': char.get('isRequired', None),
                'ktru_char_origin': char.copy(),
            }
            kkn_chars.append(char)

        worked_list.append(kkn)

    return worked_list
