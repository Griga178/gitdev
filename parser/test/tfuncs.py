# прочие функции для классов

# ПАРСЕР ВЫВОДИТ СПИСОК ИЛИ СЛОВАРЬ или проч
def my_parser():
    parsing_info = ['citi/page1:500', 'dns/page1:412.66', 'onlinetr/page1:419', 'citi/page1:501']
    return parsing_info



def pars_result_to_example(parse_str, example = False):
    result = parse_str.split(':')
    # Ссылка
    example = result[0]
    # Цена
    example = result[1]
    return example
