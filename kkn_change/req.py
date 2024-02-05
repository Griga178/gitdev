import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from bs4 import BeautifulSoup

import sys
import getpass


user_name = getpass.getuser()
sys.path.insert(1, f'C:/Users/{user_name}/Desktop/myfiles')
import gz_data
login = gz_data.login
password = gz_data.password

HEADERS = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.825 YaBrowser/23.11.1.825 (corp) Yowser/2.5 Safari/537.36',
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'ru,en;q=0.9',

    # 'Cookie'
    # 'Origin': 'https://new.gz-spb.ru',
    # 'Referer': 'https://new.gz-spb.ru/',
    # 'Sec-Ch-Ua': '"Chromium";v="118", "YaBrowser";v="23", "Not=A?Brand";v="99"',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    }
# HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0', 'accept': '*/*'}

# api_url = 'https://new.gz-spb.ru/index.php?rpctype=direct&module=default'
api_url = 'https://new.gz-spb.ru/index.php'

# p = requests.post(api_url, verify = False, headers = {'User-Agent': user_agent_val})

params = {'rpctype': 'direct', 'module': 'default'}
token_data = {
    "action": "Index",
    "method":"index",
    "data": None,
    "type":"rpc",
    "tid": 2,
    "token":""}

ya_cookies = {
    '_ym_uid':'1684738729281894556',
    '_ym_d': '1706624517'
}

import time
def current_milli_time():
    return round(time.time() * 1000)

with requests.Session() as session:
    # для получения куки
    # response = session.get(
    #     # api_url,
    #     f'https://new.gz-spb.ru/api.php?_dc={current_milli_time()}',
    #     verify = False,
    #     headers = HEADERS
    # )
    #
    # session.cookies.update(ya_cookies)
    # print(session.cookies.get_dict(), 'get')

    # Получаем токен авторизации
    response = session.post(
        'https://new.gz-spb.ru/index.php?rpctype=direct&module=default',
        verify = False,
        data = token_data,
        headers = HEADERS,
        params = params)
    #
    token = response.json()['result']['auth_token']
    print('get token:', token)

    # print(session.cookies.get_dict(), 'post -> token')
    # print(response.json())
    #
    # aip_url = 'https://new.gz-spb.ru/api.php'
    # dc_params = {'_dc': current_milli_time()}
    # resp = session.get(aip_url,
    #     verify = False,
    #     params = dc_params)
    # # print(resp)
    # print()
    # print('get -> api', session.cookies.get_dict())
    # # print(resp.json())
    #
    # # SERVER INFO
    # data_info = {"action":"Index",
    # "method":"serverinfo",
    # "data":None,
    # "type":"rpc",
    # "tid":3,
    # "token":token}
    # response = session.post(api_url,
    #     verify = False,
    #     data = data_info,
    #     headers = HEADERS,
    #     params = params)
    # print(response.json())

    auth_data = {"action":"Authentication",
        "method":"login",
        "data": [login, password, {"lock_ip":"on"}],
        # json.dumps([login, password, {"lock_ip":"on"}])
        "type":"rpc",
        "tid": 3,
        # "token": token
        }
    print(auth_data)
    #
    HEADERS['Content-Type'] = 'application/json; charset=UTF-8'
    HEADERS['Content-Length'] = '157'

    response2 = session.post(
        'https://new.gz-spb.ru/index.php?rpctype=direct&module=default',
        verify = False,
        data = json.dumps(auth_data),
        headers = HEADERS,
        params = params)
    #
    print(session.cookies.get_dict(), 'post -> login')
    # # print('post - login', session.cookies.get_dict())
    # # print()
    print(response2.json())

    # classif = {
    #     "action":"Authentication",
    #     # "method":"activate",
    #     "action":"login",
    #     # "method":"serverinfo",
    #     # "data": "",
    #     "data": [login, password],
    #     "type":"rpc",
    #     "tid": 3,
    #     "token":token
    # }
    # response2 = session.post(
    #     api_url,
    #     verify = False,
    #     data = classif,
    #     headers = HEADERS,
    #     params = params)
    # print(response2.json())
    # print(session.cookies.get_dict(), 'post -> last')



    a = {'key':'val', 'key_1': 2}
    {'key':'val','key_1':2}
    str_a = json.dumps(a)
    print(len(str_a))
