

import sys
import os

from folders import run_manager
from excel_reader import read_work_table
from console_interface import run_console_interface

run_manager()

if len(sys.argv) > 1:
    print(sys.argv[1])
    excel_info = read_work_table(sys.argv[1])
    # update_work_table(excel_info)
    print(len(excel_info[0]), len(excel_info[1]))


run_console_interface()



# def define_date():
#     """Запись текущей даты (переделка)"""
#     quarters = ["01", "02", "03", "04"]
#     print("Какой квартал: ", ", ".join(quarters))
#     chosen_qu = int(input("Введите от 1 - 4: "))
#     chosen_year = str(input("За какой год: "))
#     current_date = f'{quarters[chosen_qu - 1]}_{chosen_year}'
#     return current_date
