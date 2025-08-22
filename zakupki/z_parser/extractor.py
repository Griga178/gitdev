# extractor.py (логгирование и защищённый парсинг)

import logging
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def parse_common_data(html_content: str) -> Dict[str, Optional[object]]:
    soup = BeautifulSoup(html_content, 'html.parser')

    result = {
        'name': None,
        'unit': None,
        'dateUpdate': None,
        'ownCharsIsForbidden': None,
        'number': None,
        'version': None,
    }
    try:
        header_block = soup.find('div', class_='sectionMainInfo__header')
        header_text = header_block.get_text(strip=True)
        result['number'] = header_text
        logger.debug("Parsing header_block title=%r", header_text)
    except Exception as e:
        logger.exception("Error parsing header_block: %s", e)
    try:
        sections = soup.find_all('div', class_='cardMainInfo__section')
        logger.debug("Found %d cardMainInfo__section elements", len(sections))
        for section in sections:
            title_tag = section.find('span', class_='cardMainInfo__title')
            content_tag = section.find('span', class_='cardMainInfo__content')
            if not title_tag or not content_tag:
                logger.debug("Skipping section without title or content: %s", section)
                continue

            title_text = title_tag.get_text(strip=True)
            content_text = content_tag.get_text(strip=True)
            logger.debug("Parsing section title=%r content=%r", title_text, content_text)

            if title_text == "Обновлено":
                result['dateUpdate'] = content_text
                continue

            if title_text.startswith("Единица измерения"):
                result['name'] = content_text
                # Попытки извлечь единицу из заголовка
                for sep in (":", "—", "-", "–"):
                    if sep in title_text:
                        parts = [p.strip() for p in title_text.split(sep, 1)]
                        if len(parts) > 1 and parts[1]:
                            result['unit'] = parts[1]
                            break
                else:
                    parts = title_text.split()
                    if len(parts) >= 3:
                        result['unit'] = parts[-1]
                logger.debug("Extracted name=%r unit=%r", result['name'], result['unit'])
    except Exception as e:
        logger.exception("Error parsing common data: %s", e)

    try:
        forbidden_section = soup.find('section', class_='blockInfo__section')
        if forbidden_section:
            f_title = forbidden_section.find('span', class_='section__title')
            f_info = forbidden_section.find('span', class_='section__info')
            if f_title and f_info:
                title_txt = f_title.get_text(strip=True)
                info_txt = f_info.get_text(strip=True)
                logger.debug("Forbidden block title=%r info=%r", title_txt, info_txt)
                if title_txt == 'Указание дополнительных характеристик запрещено':
                    if info_txt == "Нет":
                        result['ownCharsIsForbidden'] = False
                    elif info_txt == "Да":
                        result['ownCharsIsForbidden'] = True
    except Exception as e:
        logger.exception("Error parsing forbidden block: %s", e)

    logger.info("Parsed result %s", result)
    return result


def parse_ktru_version(html_content: str) -> Dict[str, Optional[Any]]:
    """
    Возвращает словарь вида {"version": int | None, "date": str | None}
    date пока не парсится из HTML — оставлен для совместимости/расширения.
    """
    result: Dict[str, Optional[Any]] = {"version": None, "date": None}

    try:
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        logger.exception("parse_ktru_version: ошибка при создании BeautifulSoup")
        return result

    try:
        div = soup.find("div", id="ktruVersionContent")
        if not div:
            logger.debug("parse_ktru_version: div#ktruVersionContent не найден")
            return result

        table = div.find("table")
        if not table:
            logger.debug("parse_ktru_version: <table> внутри div не найден")
            return result

        tbody = table.find("tbody")
        all_tr = tbody.find_all("tr")
        if not all_tr:
            logger.debug("parse_ktru_version: tr в таблице не найдены")
            return result

        first_tr = all_tr[0]
        all_td = first_tr.find_all("td")
        if len(all_td) <= 2:
            logger.debug("parse_ktru_version: недостаточно td в первой строке таблицы")
            return result

        result["date"] = all_td[1].get_text(strip=True)
        text = all_td[2].get_text(strip=True)
        if not text:
            logger.debug("parse_ktru_version: текст в третьем td пустой")
            return result

        try:
            version = int(text)
            result["version"] = version
            logger.info("parse_ktru_version: найден version=%s", version)
            result["date"]
        except ValueError:
            logger.warning("parse_ktru_version: не удалось привести '%s' к int", text)
            result["version"] = None


    except Exception as e:
        logger.exception("parse_ktru_version: непредвиденная ошибка при разборе HTML")
        # возвращаем текущ recsult с None-значениями или частично заполненными полями

    return result

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

        absent_info = soup.find("span", class_="section__info")
        if absent_info and absent_info.text.strip() == "Сведения отсутствуют":
            result = [{
                "charName": ' ',
                "isRequired": False,
                "values": [],
                "unit": ' '
                }]
            return result
        else:
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
