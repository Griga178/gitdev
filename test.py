from zakupki.get_ktru_chars import get_html_content
from zakupki.get_ktru_chars import parse_ktru_chars_table_from_html
from zakupki.get_ktru_params import get_last_ktru_version
from zakupki.get_ktru_params import get_common_data

from zakupki.get_ktru_chars import BeautifulSoup

'''
парсим какие то данные КТРУ 1
парсим какие то данные КТРУ 2
парсим характеристики КТРУ
сохраняем версии в pickle файл
*тут можно посмотреть список ктру с фильтром по дате обновления
"https://zakupki.gov.ru/epz/ktru/search/results.html?morphology=on&search-filter=Дате+размещения&active=on&ktruCharselectedTemplateItem=0&sortBy=ITEM_CODE&pageNumber=1&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&updateDateFrom=01.08.2025"
'''
ktruNumber = '26.20.17.110-00000037'

ktruVersion = '10'


# I part - номер последней версии

# url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/version-journal.html?itemId={ktruNumber}'
# html_content = get_html_content(url)
# ktruVersion = get_last_ktru_version(html_content)
# print("ktruVersion =", ktruVersion)

# II part - общая инфа по КТРУ

# url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-description.html?itemId={ktruNumber}'
# html_content = get_html_content(url)
# ktru_params = get_common_data(html_content)
# print(ktru_params)


# III part
url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-part-description.html?itemVersionId={ktruNumber}_{ktruVersion}&page=1&recordsPerPage=1000&isTemplate=false&onlyRequired=false'
html_content = get_html_content(url)

data = parse_ktru_chars_table_from_html(html_content)

for item in data:
    print(item)


ktru_params = {
    'number': '',
    'name': '',
    'unit': '',
    'ownCharsIsForbidden': '',
    'version': '',
    'dateUpdate': '',
}


requests = [
    {
    "number": '26.20.17.110-00000037',
    "version": None,
    "isParse": True,
    }
]
ktru = {
    '26.20.17.110-00000037': [
        {'version': '1', ...},  #'ktru_params'
        {'version': '2', ...},  #'ktru_params'
    ]
}
