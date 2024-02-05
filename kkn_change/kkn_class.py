class KKN_Attributes():
    def __init__(self, attributes):
        '''
        attributes содержит в себе ответ от сервера на запрос
        nsi --> Classifier --> getFullClassifierCategoryAttributesData

        |-----response
        |-----|-----'result'
        |-----|-----|-----'result' []
        |-----|-----|-----|-----{'id':1, ...}
        |-----|-----|-----|-----{'id':2, ...}

        -->

        self.values = {
            'name': 'Интерфейс'|'Длинна'|'Количество портов USB'
            'from_value': None|0.01|None
            'to_value': None|1|None
            'values':['USB 2.0', ...]
            'okei_symbol': None|'М'|'ШТ'
            ...
        }

        '''

        self.values = []
        for attr in attributes:
            # Аттрибут используется в ккн
            if not attr['value']['is_no_show']:
                # сохраняем 12 характеристик (не массивы)
                temp_dict = {}
                my_attr_val = {'values':[]}
                for key, val in attr.items():

                    if key == 'dictionary':

                        if val:
                            for di in val:
                                temp_dict[di['text_value_id']] = di['name']

                    elif key == 'okei':
                        if val:
                            my_attr_val['okei_symbol'] = val['symbol']
                            my_attr_val['okei_full_name'] = val['full_name']

                    elif key == 'value':
                        for val_key, val_val in val.items():

                            if val_key == 'dictionary_values':
                                for attr_vals in val_val:

                                    my_attr_val['values'].append(temp_dict[int(attr_vals)])
                            else:
                                my_attr_val[val_key] = val_val
                    else:
                        # print(key,val)
                        my_attr_val[key] = val

                self.values.append(my_attr_val)

class KKN():
    def __init__(self, **kwargs):
        '''
            kwargs содержит в себе ответ от сервера на запрос
            nsi --> Classifier --> getClassifierNode
            примерно 28 шт

            |-----response
            |-----|-----'result'
            |-----|-----|-----'category' {}
            |-----|-----|-----|-----'id'
            |-----|-----|-----|-----'name'
            |-----|-----|-----|----- ...

        '''
        self.__dict__.update(kwargs)
        self.attributes = []

    def init_attributes(self, attributes):
        self.attributes = KKN_Attributes(attributes)

    def cmd_print(self):
        print(self.name, self.okpd2, self.detail_code)
        if self.attributes:
            for el in self.attributes.values:
                if el['attr_has_dict']:

                    print(el['name'], el['values'], end = ' ')

                else:
                    print(el['from_value'], el['to_value'], end = ' ')

                print(el.get('okei_symbol', ''))

    def to_excel(self):
        '''--> [[],[]]'''
        kkn_rows = []
        first_row = [
            None, self.id, self.name, self.okpd2, self.detail_code,
            # None, self.id, self.name, self.okpd2, None,
            self.okeiSymbol, self.product_part,
            # None, self.product_part,
            None, None, None, None, None, None,
            self.categoryName, self.is_actual, None,
            # None, self.is_actual, None,
            self.approved, self.approved_kgz,
            None, None, None,
            self.russian_goods, None
            ]
        # Характеристики заменяют 1 строку
        # от 7 элемента

        fr = False
        for el in self.attributes.values:
            attrs_vals = ''
            if not fr:
                first_row[7] = el['name']
                attrs_vals = ''
                val_counter = 0
                fr = True
                if el['attr_has_dict']:
                    for dict_attrs in el['values']:
                        val_counter += 1
                        attrs_vals += dict_attrs + '; '
                    else:
                        attrs_vals = attrs_vals[:-2]
                    if val_counter >= 1:
                        first_row[11] = attrs_vals
                    else:
                        first_row[10] = attrs_vals
                kkn_rows.append(first_row)
            else:
                cur_row = [None, None, None, None, None, None, None]
                cur_row.append(el['name'])
                val_counter = 0
                if el['attr_has_dict']:
                    for dict_attrs in el['values']:
                        val_counter += 1
                        attrs_vals += dict_attrs + '; '
                    else:
                        attrs_vals = attrs_vals[:-2]
                    if val_counter >= 1:
                        cur_row.append(None)
                        cur_row.append(None)
                        cur_row.append(None)
                        cur_row.append(attrs_vals)
                    else:
                        cur_row.append(None)
                        cur_row.append(None)
                        cur_row.append(attrs_vals)
                else:
                    fv = float(el['from_value']) if el['from_value'] else None
                    cur_row.append(fv)
                    tv = float(el['to_value']) if el['to_value'] else None
                    cur_row.append(tv)
                    cur_row.append(None)
                    cur_row.append(None)
                okei_symbol = el.get('okei_symbol', None)
                cur_row.append(okei_symbol)
                kkn_rows.append(cur_row)
        return kkn_rows
