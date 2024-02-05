class KKN_v2():
    def __init__(self, **kwargs):

        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.okpd2 = kwargs.get('okpd2', None)
        self.detail_code = kwargs.get('detail_code', None)
        self.okeiSymbol = kwargs.get('okeiSymbol', None)

        self.categoryName = kwargs.get('categoryName', None)
        self.is_actual = kwargs.get('is_actual', None)
        self.approved = kwargs.get('approved', None)
        self.approved_kgz = kwargs.get('approved_kgz', None)
        self.russian_goods = kwargs.get('russian_goods', None)

        self.attributes = []

    def add_attrs(self, value):
        self.attributes.append(KKN_Attr_v2(value))

class KKN_Attr_v2():
    def __init__(self, value):
        # 11 парам
        self.name = value.get('name', None)

        self.id = value.get('id')
        self.mte_id = value.get('mte_id', None)
        self.ktru_characteristic_id = value.get('ktru_characteristic_id', None)
        self.nsi_classifier_category_id = value.get('nsi_classifier_category_id', None)
        self.attribute_name_id = value.get('attribute_name_id', None)
        self.unit_id = value.get('unit_id', None)
        self.attr_required = value.get('attr_required', None)
        self.attr_seq_num = value.get('attr_seq_num', None)
        self.attr_type = value.get('attr_type', None)

        self.attr_has_dict = value.get('attr_has_dict', None)
        self.value = Attr_value(value['value'], value['dictionary'])

class Attr_value():
    def __init__(self, value, cat_dict):
        

dlist = [
    {'id': 22177574, 'name': "USB Flash",
    'nsi_attribute_id': 15415267, 'text_value_id': 22184853},
    {'id': 22177573, 'name': "Ethernet",
    'nsi_attribute_id': 15415267, 'text_value_id': 1509037},
    {'id': 22177573, 'name': "Ethernet",
    'nsi_attribute_id': 15415267, 'text_value_id': 1509037}
]

srch = 1509037

# for el in dlist:
    # print(el)

a = next((i for i in dlist if i.get('text_value_id') == srch), None)

print(a)
