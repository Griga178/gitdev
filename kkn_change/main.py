import requests
import requests.packages.urllib3
import json

class Main():

    def __init__(self, *args, **kwargs):
        '''            Создаем сессию
            логинимся если есть логин пароль        '''
        requests.packages.urllib3.disable_warnings()

        self.session = requests.Session()
        self.params = {
            'rpctype': 'direct',
            'module': 'default',
        }
        self.url = 'https://new.gz-spb.ru/index.php'

        response = self.session.post(
            self.url,
            verify = False,
            data = {
                "action": "Index",
                "method": "index"},
            params = self.params
            )

        self.token = response.json()['result']['auth_token']

        if kwargs.get('name') and kwargs.get('password'):
            self.login(kwargs['name'], kwargs['password'])
        if len(args) == 2:
            self.login(args[0], args[1])

    def login(self, name, password):
        ''' Авторизация '''
        auth_data = {
            "action": "Authentication",
            "method": "login",
            "data": [name, password, {"lock_ip":"on"}],
            "type":"rpc",
            "token": self.token
            }

        response = self.session.post(
            self.url,
            verify = False,
            data = json.dumps(auth_data),
            params = self.params
            )
        print(response.json())
        print()

    def get_kkns_by_name(self, kkn_name):
        self.params['module'] = 'nsi'
        data = {
            "action": "Classifier",
            "method": "getClassifierNodeGrid",
            "data": [{
                'start': 0,
                'limit': 100,
                'mode': 'all',
                'category': "",
                'parameters': {},
                'positionsQuery': kkn_name
            }],
            "type":"rpc",
            "token": self.token
            }

        response = self.session.post(
            self.url,
            verify = False,
            data = json.dumps(data),
            params = self.params
            )
        print(response.json())
        return response

    def kkn_name_from_response(self, response):
        print()
        print()
        print()
        kkn_info_dict = response.json()['result']['categories'][0]
        for key, val in kkn_info_dict.items():
            print([key], [val])

        # kkn_info_dicts = response.json()['result']['categories']
        # cou = 0
        # for kkn in kkn_info_dicts:
        #     cou += 1
        #     print(cou, kkn['name'])

    def get_kkn_chars_by_id(self, kkn_id):
        self.params['module'] = 'nsi'
        data = {
            "action": "Classifier",
            "method": "getFullClassifierCategoryAttributesData",
            "data": [{
                'nsi_classifier_category_id': None,
                'nsi_classifier_category_item_id': kkn_id,
            }],
            "type":"rpc",
            "token": self.token
            }

        response = self.session.post(
            self.url,
            verify = False,
            data = json.dumps(data),
            params = self.params
            )

        results = response.json()['result']['result']
        for el in results[0]['value']['dictionary_values']:
            print(el)

import sys
import getpass


user_name = getpass.getuser()
sys.path.insert(1, f'C:/Users/{user_name}/Desktop/myfiles')
import gz_data
login = gz_data.login
password = gz_data.password

# m = Main(login, password)

# response = m.get_kkns_by_name('Утюг электрический бытовой тип 1')
# response = m.get_kkns_by_name('')

# m.kkn_name_from_response(response)

# m.get_kkn_chars_by_id(5767826)
