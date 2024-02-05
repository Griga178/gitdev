from main import Main, json

def get_kkn_list_grid(self, **kwargs):
    self.params['module'] = 'nsi'
    data = {
        "action": "Classifier",
        "method": "getClassifierNodeGrid",
        "type":"rpc",
        "token": self.token,
        "data": [{
            'start': 0,
            'limit': 25,
            'mode': 'all',
            'category': "",
            'parameters': {},
            'positionsQuery': kwargs.get('positionsQuery', '')
        }]
    }
    response = self.session.post(
        self.url,
        verify = False,
        data = json.dumps(data),
        params = self.params
        )

    # print(response.json())
    return response.json()

def get_kkn(self, *args, **kwargs):
    self.params['module'] = 'nsi'
    data = {
        "action": "Classifier",
        "method": "getClassifierNode",
        "type":"rpc",
        "token": self.token,
        "data": [{'id': kwargs.get('id', args[0])}]
    }

    response = self.session.post(
        self.url,
        verify = False,
        data = json.dumps(data),
        params = self.params
        )

    # print(response.json())
    return response.json()

def get_kkn_attributes_by_id(self, *args, **kwargs):
    self.params['module'] = 'nsi'
    data = {
        "action": "Classifier",
        "method": "getFullClassifierCategoryAttributesData",
        "data": [{
            'nsi_classifier_category_id': None,
            'nsi_classifier_category_item_id': kwargs.get('id', args[0]),
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
    # print(response.json())
    return response.json()

Main.get_kkn_list_grid = get_kkn_list_grid
Main.get_kkn = get_kkn
Main.get_kkn_attributes_by_id = get_kkn_attributes_by_id

from main import login, password

m = Main(login, password)

'''
    Собираем инфу по ккн
'''

from kkn_class import KKN

# node_resp = m.get_kkn(id)
kkn_names = 'Утюг'
# node_resp = m.get_kkn_list_grid(positionsQuery = kkn_names)
# kkn = KKN(**node_resp['result']['categories'][0])
node_resp = m.get_kkn('2191276')
kkn = KKN(**node_resp['result']['category'])
response = m.get_kkn_attributes_by_id(kkn.id)
attributes = response['result']['result']
kkn.init_attributes(attributes)
# print(kkn.__dict__)
print()
# for
# print(kkn.attributes.__dict__)

# kkn.cmd_print()
print(kkn.attributes.__dict__)

from gz_xlsx import make_excel

# make_excel(kkn.to_excel())

'''
4 столба заменить истина/ложь на да/нет
тип характеристики кач/колич
'''
