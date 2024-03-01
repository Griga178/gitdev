# import re
# import time
# import os, psutil
# process = psutil.Process()
# print(process.memory_info().rss)
# start_time = time.time()
#
# def define_numbers(str_number: str) -> int:
#     str_numbers = re.findall(r'one|zero', str_number)
#
#     number = ''
#     for el in str_numbers:
#         if el == 'one':
#             number += '1'
#         elif el == 'zero':
#             number += '0'
#
#     # print(int(number))
#     return int(number)
#
# def compare_numbers(a: int, b: int) -> str:
#     if a > b:
#         return '>'
#     elif a < b:
#         return '<'
#     elif a == b:
#         return '='
#     else:
#         return 'ERROR'
#
#
# # a = define_numbers('one')
# a = define_numbers('onezerozerozerozero')
# b = define_numbers('onezerozerozerozero')
# # a = define_numbers('zero')
# # b = define_numbers('zero')
# # define_numbers('onezero')
# # define_numbers('onezeroonezero')
#
#
# print(compare_numbers(a, b))
# end_time = time.time() - start_time
# print(end_time)

# from memory_profiler import memory_usage
# print(memory_usage())
'''
Работа:
WARNING: unsatisfiable dependency!
group tests/full listed before group tests/samples!
'''
# import re
#
# def define_numbers(str_number):
#     str_numbers = re.findall(r'one|zero', str_number)
#     number = ''
#     for el in str_numbers:
#         if el == 'one':
#             number += '1'
#         elif el == 'zero':
#             number += '0'
#     return int(number)
# def compare_numbers(a, b):
#     if a > b:
#         return '>'
#     elif a < b:
#         return '<'
#     elif a == b:
#         return '='
#     else:
#         return 'ERROR'
#
# a = define_numbers(input())
# b = define_numbers(input())
# print(compare_numbers(a, b))
# print(memory_usage())

#  Принятая версия ОК
def define_numbers_2(str_number):
    number = ''
    str_row = ''
    for l in str_number:
        str_row += l
        if str_row == "one":
            number += '1'
            str_row = ''
        elif str_row == "zero":
            number += '0'
            str_row = ''

    return int(number)

a = define_numbers_2(input())
b = define_numbers_2(input())

if a > b:
    print('>')
elif a < b:
    print('<')
elif a == b:
    print('=')
