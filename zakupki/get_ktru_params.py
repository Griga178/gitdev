from bs4 import BeautifulSoup
from typing import Optional

def get_last_ktru_version(html_content: str) -> Optional[int]:
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим div с id="ktruVersionContent"
    div = soup.find('div', id='ktruVersionContent')

    ktruVersion = None
    if div:
        # Извлекаем таблицу, tbody, первую строку (tr) и третий столбец (td)
        table = div.find('table')
        if table:
            tbody = table.find('tbody')
            if tbody:
                all_tr = tbody.find_all('tr')
                if all_tr and len(all_tr) > 0:
                    all_td = all_tr[0].find_all('td')
                    if all_td and len(all_td) > 2:
                        # Получаем текст из третьего td, убираем пробелы и конвертируем в int
                        text = all_td[2].get_text(strip=True)
                        try:
                            ktruVersion = int(text)
                        except ValueError:
                            ktruVersion = None
    return ktruVersion

def get_common_data(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    result = {
        'name': None,
        'unit': None,
        'dateUpdate': None,
        'ownCharsIsForbidden': None,
        'number': None,
        'version': None,
    }
    sections = soup.find_all('div', class_='cardMainInfo__section')

    for section in sections:
        # Находим span с классом cardMainInfo__title и cardMainInfo__content внутри одного div
        titles = section.find_all('span', class_='cardMainInfo__title')
        content = section.find('span', class_='cardMainInfo__content')

        # Соответствие: сколько span title, столько и content в одной последовательности
        content_text = content.get_text(strip=True)
        title_text = titles[0].get_text(strip=True)

        if title_text == "Обновлено":
            result['dateUpdate'] = content_text
        elif title_text.startswith("Единица измерения"):
            # Получаем имя и единицу измерения
            result['name'] = content_text
            # Берём второе слово из заголовка "Единица измерения ..."
            unit_parts = title_text.split()
            if len(unit_parts) > 2:
                result['unit'] = unit_parts[2]

    forbiddenSection = soup.find('section', class_='blockInfo__section')
    if forbiddenSection:
        fTitle = forbiddenSection.find('span', class_='section__title')
        fInfo = forbiddenSection.find('span', class_='section__info')
        if fTitle.get_text(strip=True) =='Указание дополнительных характеристик запрещено':
            isForbiddenSection = fInfo.get_text(strip=True)
            if isForbiddenSection == "Нет":
                result['ownCharsIsForbidden'] = False
            elif isForbiddenSection == "Да":
                result['ownCharsIsForbidden'] = True

    return result
