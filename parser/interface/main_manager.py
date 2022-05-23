import sys
sys.path.append('module_data_base')
sys.path.append('module_parser')

from query_for_parsing import get_links_by_string_to_parser, get_links_by_id_to_parser
from manager_parser import start_parse

links = [
'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-602-chernyi-zheltyi-b0031033-1121815/',
'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-603-zheltyi-chernyi-3vt-b0031034-1121816/',
'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-601-chernyi-oranzhevyi-3-05vt-b0031036-1121812/',
'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-604-zheltyi-chernyi-3vt-b0031035-1121817/',
'https://www.citilink.ru/product/akkumulyatornyi-fonar-era-pa-602-chernyi-zheltyi-b0031033-1121815/',
'https://spb.ledpremium.ru/catalog/day_white_foodlight/prozhektor_71_656_ofl_10_4k_bl_ip65_led_10vt_ip65_4000k_onlayt_71656/',
'https://spb.ledpremium.ru/catalog/day_white_foodlight/prozhektor_61_947_ofl_100_4k_bl_ip65_led_onlayt_61947/'
]

links_id = [655, 656, 657, 658, 500]
# dict_to_parse = get_links_by_string_to_parser(links)
dict_to_parse = get_links_by_id_to_parser(links_id)


# b = start_parse(dict_to_parse)
# print(b)
