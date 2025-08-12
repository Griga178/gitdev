import requests
from bs4 import BeautifulSoup

def get_html_content(url):

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешность запроса
        return response.text
    except requests.RequestException as e:
        return f"Ошибка при получении страницы: {e}"

def parse_ktru_chars_table_from_html(html_content: str) -> list[dict,...]:
    """
    Парсит таблицу из html_content при условии, что есть тег <table>.

    Структура таблицы:
    - или 3 столбца: характеристика (с rowspan), значение (по строкам), ед. измерения
    - или 2 столбца: значение (по строкам), ед. измерения

    Args:
        html_content (str): HTML-код страницы со встроенной таблицей = response.text

    Returns:
        list of dict: список словарей с ключами:
        "charName", "isRequired", "unit", "values"(:List[str,..])

    Исключение:
        ValueError если тег <table> отсутствует
    """
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    if table is None:
        print(soup)
        raise ValueError("Тег <table> не найден в html_content")

    tbody = table.find("tbody")

    rows = tbody.find_all("tr")

    result = []
    current_characteristic = None
    char_rows_amount = 0

    for tr in rows:
        cols = tr.find_all("td")
        # Первый столбец: характеристика (только в первой строке с этой группой, остальное пропускаем)
        char_td = cols[0]
        # Если есть td с rowspan, значит новая характеристика
        if char_td.has_attr("rowspan"):

            divs = char_td.find_all("div")
            charName = divs[0].get_text(strip=True) # Название характеристики
            text_in_second_div = divs[1].get_text(strip=True) if len(divs) > 1 else ""
            isRequired = not ("не является" in text_in_second_div)

            char_rows_amount = int(char_td.get("rowspan"))

            # raw_value будет строкой с пробелами между элементами
            raw_value = cols[1].get_text(strip=True, separator=' ')
            # Далее устраним лишние пробелы и заменим неразрывные пробелы на обычные
            value = ' '.join(raw_value.split()).replace('\xa0', ' ')
            unit = cols[2].get_text(strip=True)

            current_characteristic = {
                "charName": charName,
                "isRequired": isRequired,
                "values": [value],
                "unit": unit
                }
            result.append(current_characteristic)
            char_rows_amount -= 1
        else:
            # raw_value будет строкой с пробелами между элементами
            raw_value = cols[0].get_text(strip=True, separator=' ')
            # Далее устраним лишние пробелы и заменим неразрывные пробелы на обычные
            value = ' '.join(raw_value.split()).replace('\xa0', ' ')
            current_characteristic['values'].append(value)
            char_rows_amount -= 1

    return result
