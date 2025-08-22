
def compare_ktru_chars(new_ktru, old_ktru):
    """
    Сравнивает характеристики ('chars') из двух версий KTRU и добавляет в каждую характеристику информацию о различиях.

    Принимает:
        new_ktru (dict) — объект новой версии KTRU, содержащий ключ 'chars' со списком характеристик.
        old_ktru (dict) — объект старой версии KTRU, содержащий ключ 'chars' со списком характеристик.

    Возвращает:
        dict — обновленный объект new_ktru, в котором каждая характеристика из 'chars' дополнена ключом 'version_data' с информацией:
            - Если характеристика присутствует и значения совпадают: {'isChanged': False}
            - Если характеристика присутствует, но значения отличаются: {'isChanged': True, 'new_val': [...], 'delete_val': [...]}
            - Если характеристика новая (отсутствовала в old_ktru): {'isNew': True}
            - Если характеристика удалена (есть в old_ktru, но отсутствует в new_ktru): добавляется отдельно с пустыми значениями и {'isDelete': True}

    Структура new_ktru['version_data']:
        {'isChanged': True,
         'new_val': [...], 'delete_val': [...],
        {'isNew': True,
        {'isDelete': True,
    """
    # Копия списка chars старой версии для отслеживания удаленных
    old_chars = old_ktru['chars'].copy()
    old_chars_map = {char['name']: char for char in old_chars}

    result_chars = []

    # Проходим по новым характеристикам
    for new_char in new_ktru['chars']:
        name = new_char['name']
        new_values = set(new_char['values'])
        version_data = {'isDelete': False, 'isNew': False, 'isChanged': False, 'new_val': [], 'delete_val': []}
        if name in old_chars_map:
            old_char = old_chars_map[name]
            old_values = set(old_char['values'])

            if new_values == old_values:
                # Значения совпадают
                # version_data = {'isChanged': False}
                pass
            else:
                # Есть изменения
                version_data['isChanged'] = True
                version_data['new_val'] = list(new_values - old_values)
                version_data['delete_val'] = list(old_values - new_values)

            # Удаляем из old_chars_map найденный чар для отслеживания удаления
            old_chars_map.pop(name)

            # Добавляем к чару новую информацию
            new_char['version_data'] = version_data
            result_chars.append(new_char)

        else:
            # Новый чар, которого не было раньше
            version_data['isNew'] = True
            new_char['version_data'] = version_data
            result_chars.append(new_char)

    # Все оставшиеся характеристики в old_chars_map — удалены из новой версии
    for del_char in old_chars_map.values():
        del_char_copy = del_char.copy()
        # del_char_copy['values'] = []  # пустые значения

        del_char_copy['version_data'] = {'isDelete': True, 'isNew': False, 'isChanged': False, 'new_val': [], 'delete_val': []}
        result_chars.append(del_char_copy)

    # Кладём обратно обновленный список в new_ktru
    new_ktru['chars'] = result_chars
    return new_ktru
