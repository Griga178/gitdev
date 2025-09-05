from bs4 import BeautifulSoup
import re

# Функция для рекурсивного поиска target_point
def find_target_point(soup_obj, rule):
    tag = rule.get("tag_name")
    attr_name = rule.get("attr_name")
    attr_value = rule.get("attr_value")
    index = rule.get("search_index", 0)
    target_point = rule.get("target_point")
    expected_amount = rule.get("expected_amount", None)
    recursive = rule.get("recursive", True)

    # Выбираем элементы по тегу и атрибуту (если указан)
    if attr_name and attr_value:
        elems = soup_obj.find_all(tag, attrs={attr_name: attr_value}, recursive=recursive)
    elif attr_name and not attr_value:
        # Найти все теги {tag}, у которых есть {attr_name} с любым значением
        elems = soup_obj.find_all(tag, attrs={attr_name: True}, recursive=recursive)
    else:
        elems = soup_obj.find_all(tag, recursive=recursive)

    if not elems or len(elems) <= index:
        return None

    if expected_amount:
        if len(elems) != expected_amount:
            # искомый элемент отсутствует
            return None

    elem = elems[index]

    # Если target_point True - вернем этот элемент
    if target_point is True:
        return elem
    # Если target_point - следующий уровень поиска
    elif isinstance(target_point, dict):
        return find_target_point(elem, target_point)
    else:
        return elem

def parse_html(html_content: str, settings: dict) -> dict:
    """
        получение данных из веб страницы

        html_content - html документ

        settings - настройки для поиска данных, ключи:
            смотреть в readME

        возможные варианты rules
        1 - данные ищем по тегу - блок уникальных для всех страниц
        2 - искомый блок повторяется несколько раз, по этому сначала ищем уникальный блок-родитель
        3 - искомы блок не уникален значения атрибутов могут меняться - ищем все, выбираем по индексу

    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results = {}

    for item in settings.get("search_data", []):
        name = item.get("name")
        r = item.get("rules", {})

        target_elem = find_target_point(soup, r)
        if not target_elem:
            results[name] = None
            continue

        text = target_elem.get_text(strip=True)

        # Преобразование типа
        if item.get("type") == "float":
            try:
                # Убираем все кроме цифр и точек, например, "1 234.56" -> "1234.56"
                number = re.sub(r'[^\d,.\-]', '', text).replace(',', '.')
                value = float(number)
            except:
                value = None
        elif item.get("type") == "str":
            value = text
        else:
            value = text

        results[name] = value

    return results
