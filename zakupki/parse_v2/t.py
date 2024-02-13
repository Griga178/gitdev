import requests
from bs4 import BeautifulSoup
import re
url = 'https://zakupki.gov.ru/epz/contract/search/results.html'



params = {
    'morphology': 'on',
    'search-filter': 'Дате размещения',
    # 'search-filter': 'Цене',
    'fz44': 'on',
    # 'contractStageList_0': 'on',
    'contractStageList_1': 'on',
    # 'contractStageList_2': 'on',
    # 'contractStageList_3': 'on',
    # 'contractStageList': '0%2C1%2C2%2C3',
    'contractStageList': 1,
    'contractCurrencyID': -1,
    'budgetLevelsIdNameHidden': '{}',
    'contractDateFrom': '30.12.2023',
    'contractDateTo': '02.02.2024',
    'sortBy': 'UPDATE_DATE',
    'pageNumber': '1',
    'sortDirection': 'false',
    'recordsPerPage': '_50', #_10, _20, _50
    'showLotsInfoHidden': 'false',
    }


url = 'https://zakupki.gov.ru/epz/contract/search/results.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }


session = requests.Session()
fr = session.get(
    url,
    headers = headers)
print(fr)
resp = session.get(
    url,
    headers = headers,
    params = params,
    )


# print(resp.url)
print(resp)
# print(resp.status_code)
# print(resp.status_code == 404)

if resp.status_code == 200:

    soup = BeautifulSoup(resp.text, 'html.parser')
    mydivs = soup.find("div", {"class": "search-results__total"})

    contract_amount = int(''.join(re.findall(r'\d', mydivs.string)))
    print(contract_amount)

# https://zakupki.gov.ru/epz/contract/search/results.html
# ?morphology=on
# &search-filter=Цене
# &fz44=on
# &contractStageList_1=on
# &contractStageList=1
# &contractCurrencyID=-1
# &budgetLevelsIdNameHidden=%7B%7D
# &contractDateFrom=01.01.2024
# &contractDateTo=31.01.2024
# &sortBy=PRICE
# &pageNumber=1
# &sortDirection=false
# &recordsPerPage=_50
# &showLotsInfoHidden=false
