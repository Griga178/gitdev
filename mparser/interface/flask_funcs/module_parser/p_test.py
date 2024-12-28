# 'defender_message': {'tag': 'h1', 'attr_val': 'Проверка безопасности'},
from manager_parser import start_parse

final_result_output_dict = {
    1:{
    # "shop_name": "https://www.citilink.ru",
    'need_selenium': False,
    'headless_mode': True,
    "links": {
        1: 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N',
        2: 'https://www.citilink.ru/product/monitor-igrovoi-samsung-c27g54tqwi-27-chernyi-lc27g54tqwixci-1444512/',
        3: 'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-602-chernyi-zheltyi-b0031033-1121815/'
        },
    'tag_setting': {
        'price':{'tag': 'span', 'attr': 'class', 'attr_val': 'ProductHeader__price-default_current-price'},
        'name': {'tag': 'h1', 'attr': 'class', 'attr_val': 'ProductHeader__title'},
        'sold_out': {'tag': 'h2', 'attr': 'class', 'attr_val': 'ProductHeader__not-available-header'},
        },
    },
    2:{
    "shop_name": "www.kns.ru",
    'headless_mode': True,
    'need_selenium': False,
    "links": {
        1: 'https://www.kns.ru/product/faks-panasonic-kx-fl423ruw/',
        2: 'https://www.kns.ru/product/telefon-panasonic-kx-ts2382ruw/'
        },
    'tag_setting': {
        'price': {'tag': 'span', 'attr': 'class', 'attr_val': 'price-org'},
        'name': {'tag': 'h1', 'attr': 'itemprop', 'attr_val': 'name'},
        'sold_out': {'tag': 'span', 'attr': 'class', 'attr_val': 'statpic-15'},
        },
    },
    3:{
    "shop_name": "www.onlinetrade.ru",
    'need_selenium': True,
    'headless_mode': False,
    "links": {
        1: 'https://www.onlinetrade.ru/catalogue/smartfony-c13/zte/smartfon_zte_blade_a51_lite_2_32gb_zelenyy_zte_a51.lite.gn-2768952.html',
        21: 'https://www.onlinetrade.ru/catalogue/smartfony-c13/zte/smartfon_zte_blade_a51_lite_2_64gb_zelenyy_zte_a51.lite.gn-2768952.html'
        },
        'tag_setting': {
            'price': {'tag': 'div', 'attr': 'class', 'attr_val': 'catalog__displayedItem__actualPrice'},
            'name': {'tag': 'h1', 'attr': 'itemprop', 'attr_val': 'name'},
            'sold_out': False
            },
    },
}

def count_links_amount(input_dict):
    comon_amount = 0
    for shop_id, shops_settings in input_dict.items():
        for link_id, link_settings in shops_settings['links'].items():
            comon_amount += 1
    return comon_amount

def pretty_print(dict_output):
    print(dict_output)
    print('КРАСИВЫЙ ВЫВОД***:')
    for shop_id, links_result in dict_output.items():
        print(' ', shop_id)
        for link_id, link_info in links_result.items():
            if link_info:
                print('     №', link_id)
                if link_info:
                    print('     дата:', link_info['current_date'])
                if link_info['current_name']:

                    first_str = link_info['current_name']
                else:
                    first_str = f'Ошибка имени: '
                if link_info['current_price']:
                    second_str = link_info['current_price']
                else:
                    second_str = f'Нет в наличии: {link_info["current_sold_out"]}'

                print(first_str)
                print(second_str)


# текущий вывод
{1:
    {1:
        {'current_price': 5290.0,
        'current_name': 'ИБП PowerCom Spider SPD-1000N, 1000ВA',
        'current_sold_out': False},
    2: {'current_price': 27790.0,
        'current_name': 'Монитор игровой Samsung C27G54TQWI 27" черный [lc27g54tqwixci]',
        'current_sold_out': False}, 3: {}}}


# pretty_print(start_parse(final_result_output_dict))
# count_links_amount(final_result_output_dict)
