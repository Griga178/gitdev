''' поиск по ИНН/ОГРН адреса, названия  '''

ogrn = '1187746871157'
import requests
import json


def get_info(number):
    query_param = {
        'query': f'{number}',
    }
    url = 'https://egrul.nalog.ru/'


    sess = requests.Session()

    resp = sess.post(url, data = query_param)
    resp_1 = resp.json()

    my_code = resp_1['t']

    url_2 = 'https://egrul.nalog.ru/search-result/' + my_code

    resp_2 = sess.get(url_2)

    response = resp_2.json()['rows'][0]

    d_return = {
        'address': response.get('a'),
        'name': response.get('c'),
        'manager': response.get('g'),
        'inn': response['i'],
        'full_name': response['n'],
        'ogrn': response['o'],
        'date': response['r'],
        'kpp': response.get('p'),
    }
    # for k, v in d_return.items():
    #     print(k, v)

    return d_return

# get_info(ogrn)
# get_info(321183200042413)
