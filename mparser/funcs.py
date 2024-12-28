import requests
from bs4 import BeautifulSoup

def catalog_parse(catalog_link: str, rules: dict) -> list:

    card_links = []

    page = requests.get(catalog_link)

    soup = BeautifulSoup(page.text, "html.parser")

    if page.status_code == 200:
        target_1 = soup.find(
            rules['curent_count']['tag_name'], rules['curent_count']['tag_val'])
        target_2 = soup.find(
            rules['total_count']['tag_name'], rules['total_count']['tag_val'])
        curent_count = float(target_1.text)
        total_count = float(target_2.text)
    else:
        return None

    temp_1 = total_count // curent_count # 10
    temp_2 = total_count / curent_count # 10.5

    if temp_2 > temp_1:
        page_count = int(temp_1 + 1)
    else:
        page_count = int(temp_1)

    print(page_count)

    if rules['iter_by_url']:
        for i in range(page_count):
            next_url = catalog_link + rules['url_start_part'] + str(i + 1) + rules['url_end_part'] + '/'
            print(next_url)

            '''
                ПАРСИНГ МИНИ КАРТОЧКИ (СОКРАЩЕННОЙ ИНФЫ)
            '''
    cards = soup.find_all('div', {'class': 'goods-list-item mx-auto'})
    print(cards[0])

     # next


    return card_links

def card_parse(card_link: str) -> list:

    # read_page

    # save

    pass
