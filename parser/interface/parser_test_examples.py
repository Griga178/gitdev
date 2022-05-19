from copy import copy
base_set = {
'need_selenium': True,
'headles_mode': False,
'price': False,
'name': False,
'sold_out_tag': False,
'sold_out_mes': False,
'defender_message': False,
'headless_mode': True
}

# СИТИЛИНК
link_set_1 = {
'need_selenium': False,
'price':{'tag': 'span', 'attr': 'class', 'attr_val': 'ProductHeader__price-default_current-price'},
'name': {'tag': 'h1', 'attr': 'class', 'attr_val': 'ProductHeader__title'},
'sold_out_tag': {'tag': 'div', 'attr': 'class', 'attr_val': 'ProductHeader__price'},
'sold_out_mes': 'Нет в наличии'
}
settings_dict_1 = copy(link_set_1)
settings_dict_2 = copy(link_set_1)

settings_dict_1['http_link'] = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
settings_dict_2['http_link'] = 'https://www.citilink.ru/product/monitor-igrovoi-samsung-c27g54tqwi-27-chernyi-lc27g54tqwixci-1444512/'

# КНС
link_set_2 = {
'need_selenium': False,
'price': {'tag': 'span', 'attr': 'class', 'attr_val': 'price-org'},
'name': {'tag': 'h1', 'attr': 'itemprop', 'attr_val': 'name'},
'sold_out_tag': {'tag': 'div', 'attr': 'class', 'attr_val': 'goods-status'},
'sold_out_mes': 'снят с производства'
}
settings_dict_3 = copy(link_set_2)
settings_dict_4 = copy(link_set_2)

settings_dict_3['http_link'] = 'https://www.kns.ru/product/faks-panasonic-kx-fl423ruw/'
settings_dict_4['http_link'] = 'https://www.kns.ru/product/telefon-panasonic-kx-ts2382ruw/'

# ОНЛАЙНТРЕЙД
link_set_3 = copy(base_set)
link_set_3['price'] = {'tag': 'div', 'attr': 'class', 'attr_val': 'catalog__displayedItem__actualPrice'}
link_set_3['name'] = {'tag': 'h1', 'attr': 'itemprop', 'attr_val': 'name'}

settings_dict_5 = copy(link_set_3)
settings_dict_5['http_link'] = 'https://www.onlinetrade.ru/catalogue/smartfony-c13/zte/smartfon_zte_blade_a51_lite_2_32gb_zelenyy_zte_a51.lite.gn-2768952.html'
settings_dict_5['defender_message'] = {'tag': 'h1', 'attr_val': 'Проверка безопасности'}
settings_dict_5['headless_mode'] = False
