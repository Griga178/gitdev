# main.py
"""


на вход: [ktru_str, ...]

выход [{
    "name": "ktru_name_str",
    "chars": [
        "char_name": "name_str"
        "values": []
        ],
    ...
    }, ...]
"""

# from controller.controller import Controller
from services.business import fetch_parse_and_store_ktru
def main():
    # Создаём контроллер (можно передать конфиг)
    # ctrl = Controller(config={"env": "dev"})
    #
    # # Инициализация компонентов
    # ctrl.init_db()
    # ctrl.init_parser() # текущая работа
    # ctrl.init_services()

    # Простой запуск пайплайна для одного источника
    valid_ktru_number = '26.20.17.110-00000037'
    # print('ctr ', ctrl)
    result = fetch_parse_and_store_ktru(valid_ktru_number)
    print("code is over")
    for i in result['chars'][0]:
        print(i)
    #
    # for el in result['chars']:
    #     print(el)


if __name__ == "__main__":
    main()

"""
есть список из [ktru_dict, ...]
имена ключей ktru_dict и типы значений [
    ktru_id:int,
    name:str,
    number:str,
    version:int,
    chars_count:int,
    chars:list[ktru_char, ...]]
имена ключей chars и типы значений [
    id:int,
    ktruVersionId:int,
    name:str,
    unit:str,
    isRequired:bool,
    values:list[str,...]]
"""
