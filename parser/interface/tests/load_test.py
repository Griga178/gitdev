import sys
sys.path.append('../')

from flask_funcs.module_data_base.sql_start import *

from flask_funcs.file_loader.excel_reader import parse_file_links

from flask_funcs.file_loader.sql_query import replace_kkn_name_kkn_id, replace_link_name_link_id

# file_name = 'C:/Users/G.Tishchenko/Desktop/26 Театр.xlsx'
file_name = '26 Театр.xlsx'

excel_dect = parse_file_links(file_name)

dict_step_2 = replace_kkn_name_kkn_id(excel_dect)

res = replace_link_name_link_id(dict_step_2)

print(res)
