'''

    ВОЗЧОЖНО ЧЕРНОВИК

'''
import requests
import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()
import json
from bs4 import BeautifulSoup

login = '1'
password = '0'
url = 'http://srv07/cmec/Login.aspx'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
with requests.Session() as session:

    response = session.get(url, headers = HEADERS, verify = False)

    root = BeautifulSoup (response.text, 'html.parser')

    # __VIEWSTATE = root.find('input', {'id': '__EVENTVALIDATION'})['value']
    # print(__VIEWSTATE)

    form_data = {
        '__VIEWSTATE': root.find('input', {'id': '__VIEWSTATE'})['value'],
        '__VIEWSTATEGENERATOR': root.find('input', {'id': '__VIEWSTATEGENERATOR'})['value'],
        '__EVENTVALIDATION': root.find('input', {'id': '__EVENTVALIDATION'})['value'],
        'ctl00$FasContent$TextLogin': login,
        'ctl00$FasContent$TextPassword': password,
        'ctl00$FasContent$TextAddLogin': '', # empty
        'ctl00$FasContent$ButtonLogin': 'Войти',
    }
    params = {
        'wintype': 'window_desktops',
        'ReturnUrl': '/cmec/CA/Desktop/Default.aspx?wintype=window_desktops'
        }

    response = session.post(
        url,
        headers = HEADERS,
        verify = False,
        data = json.dumps(form_data),
        params = params)
    # print(response.text)
    url_2 = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops'
    response = session.get(url_2, headers = HEADERS, verify = False)


    main_page = root = BeautifulSoup (response.text, 'html.parser')

    print(main_page.title)
    user_name = main_page.find('div', {'wbkey': 'userMenu'})#['wbtitle']
