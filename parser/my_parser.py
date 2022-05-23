
# НАБОР УПРАВЛЯЮЩИХ ФУНКЦИЙ
# 1 ВЫБОР ИСТОЧНИКА ССЫЛОК (1 ИЗ ФАЙЛА, 2 ИСКАТЬ НА САЙТЕ)
# 2 ИЗУЧЕНИЕ САЙТА (НАХОЖДЕНИЕ КАТАЛОГА, ОСНОВНЫЕ ТЕГИ (ЦЕНА, НАЛИЧИЕ, ЗАГОЛОВКИ))
# 3 ПАРСИНГ ЦЕН, НАЛИЧИЯ, ХАРАКТЕРИСТИК.
# 4 ЗАПИСЬ В БД
# * ЗАПИСЬ МОДЕЛИ И ЕЕ ХАРАКТЕРИСТИК В БД
# * ПАРСИНГ ИНФОРМАЦИОННЫХ САЙТОВ


"""Описание словаря каталога:
    ключ - название сайта = главная стр - http://
    значение - СПИСОК инфы каталога данного сайта
----------------------------------------
        1 ссылка на каталог (корень)
        2 список тегов для определения блока с каталожным наименования
        3 СЛОВАРЬ подкаталогов
----------------------------------------
            ключ - название товара/группы товаров
                если тип значения СПИСОК:
                    значение = [ссылка на группу т., словарь товаров]
                в противном случае
                    значение = СЛОВАРЬ товаров (там такая же схема)
----------------------------------------
                ключ - название товара/группы товаров
                значение - (str, либо если окажется группой: [str, dict])

{"www.citilink.ru":
    ["https://www.citilink.ru/catalog/",
    ['li', 'class', 'CatalogLayout__item-list'],
    {"Смартфоны и гаджеты":['https://www.citilink.ru/catalog/smartfony-i-gadzhety/'
            {"Смартфоны": "https://www.citilink.ru/catalog/smartfony/",
            "Сотовые телефоны": "https://www.citilink.ru/catalog/sotovye-telefony/",
            "Планшеты": "https://www.citilink.ru/catalog/planshety/"}]
    "Бытовая техника для дома и кухни":['https://www.citilink.ru/catalog/bytovaya-tehnika-dlya-doma-i-kuhni/'
            {"Крупная бытовая техника": ["https://www.citilink.ru/catalog/krupnaya-bytovaya-tehnika/"
                                        {'Винные шкафы': "https://www.citilink.ru/catalog/vinnye-shkafy/",
                                        'Холодильники': 'https://www.citilink.ru/catalog/holodilniki/'}],
            "Встраиваемая техника": "https://www.citilink.ru/catalog/vstraivaemaya-tehnika/"}]
    }
    ]
}
"""
catalog_dict = {"www.citilink.ru":["https://www.citilink.ru/catalog/", ['li', 'class', 'CatalogLayout__item-list'],
        {"Смартфоны и гаджеты":['https://www.citilink.ru/catalog/smartfony-i-gadzhety/', {"Смартфоны": "https://www.citilink.ru/catalog/smartfony/",
        "Сотовые телефоны": "https://www.citilink.ru/catalog/sotovye-telefony/", "Планшеты": "https://www.citilink.ru/catalog/planshety/"}],
        "Бытовая техника для дома и кухни":['https://www.citilink.ru/catalog/bytovaya-tehnika-dlya-doma-i-kuhni/',
        {"Крупная бытовая техника": ["https://www.citilink.ru/catalog/krupnaya-bytovaya-tehnika/", {'Винные шкафы': "https://www.citilink.ru/catalog/vinnye-shkafy/",
        'Холодильники': 'https://www.citilink.ru/catalog/holodilniki/'}], "Встраиваемая техника": "https://www.citilink.ru/catalog/vstraivaemaya-tehnika/"}]}]}
