import sys
sys.path.append('../')

from flask_funcs.module_data_base.sql_start import *

from flask_funcs.file_loader.excel_reader import parse_file_links

from flask_funcs.file_loader.sql_query import check_kkn_in_db

file_name = 'C:/Users/G.Tishchenko/Desktop/26 Театр.xlsx'

excel_dect = parse_file_links(file_name)

res = check_kkn_in_db(excel_dect)

print(res)
