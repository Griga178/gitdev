'''

    ВОЗЧОЖНО ЧЕРНОВИК

'''
import requests
import requests.packages.urllib3
import json

requests.packages.urllib3.disable_warnings()

import sys
import getpass


user_name = getpass.getuser()
sys.path.insert(1, f'C:/Users/{user_name}/Desktop/myfiles')
import gz_data
login = gz_data.login
password = gz_data.password


gz_uri = 'https://new.gz-spb.ru/index.php?rpctype=direct&module=default'

session = requests.Session()
# with requests.Session() as session:
# Получаем токен авторизации
response = session.post(
    'https://new.gz-spb.ru/index.php?rpctype=direct&module=default',
    verify = False,
    data = {
        "action": "Index",
        "method": "index"},
    )

token = response.json()['result']['auth_token']
print('get token:', token)
# Входим
auth_data = {
    "action": "Authentication",
    "method": "login",
    "data": [login, password, {"lock_ip":"on"}],
    "type":"rpc",
    "token": token
    }
response = session.post(
    'https://new.gz-spb.ru/index.php?rpctype=direct&module=default',
    verify = False,
    data = json.dumps(auth_data)
    )

print(response.json())

get_kkn = {
    "action":"Classifier",
    "method":"getClassifierNode",
    "data":[{"id":5767826}],
    "type":"rpc",
    "token": token
}

response = session.post(
    'https://new.gz-spb.ru/index.php?rpctype=direct&module=nsi',
    verify = False,
    data = json.dumps(get_kkn))

print(response.json())
get_kkn_card = [{
    "action":"Classifier",
    "method":"getFullClassifierCategoryAttributesData",

    "data":[{
        'nsi_classifier_category_id':None,
        "nsi_classifier_category_item_id":5767826}],
    "type":"rpc",
    "token": token
},
{
    "action":"Classifier",
    "method":"classifierCategorySearch",
    "data":[{'actual': True, 'plain': True, 'query': "3D-принтеры"}],
    "type":"rpc",
    "token": token
},
{
    "action":"Ktru",
    "method":"search",
    "data":[{
        'okpd2_code': "26.20.16.121",
        'loadid': 92150, 'plain': True,
        'is_not_template': True,
        'query': "92150"}],
    "type":"rpc",
    "token": token
},
{
    "action":"Attribute",
    "method":"getOKEY",
    "data": None,
    "type":"rpc",
    "token": token
},
]
response = session.post(
    'https://new.gz-spb.ru/index.php?rpctype=direct&module=nsi',
    verify = False,
    data = json.dumps(get_kkn_card))
print()
print()
# print(response.json())

for list_el in response.json():
    print(list_el['result'])
    print()
