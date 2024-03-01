# from .main import Parser_ver_2
from .main import *

'''
    Добавление функций к парсеру
    парсинг инфы из карточки контракта
'''
def read_product_page(self):
    pass

def get_product_page(self, contruct_number):
    payment_url = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order-list.html'
    pr_param = {
        'reestrNumber': contruct_number,
        'page': 1,
        'pageSize': 50
    }
    print('Запрос к:', contruct_number)
    product_page = self.session.get(
        payment_url,
        headers = self.headers,
        params = pr_param)
    print(product_page)
    # //span[@class='tableBlock__resultTitle']
    pr_count = get_product_amount(product_page)

    parsed_rows = get_data_from_product_table(product_page, contruct_number)

    counter_parsed_product = 0
    print(parsed_rows)
    print(pr_count)

def parse_products(self):
    '''
    Парсинг товаров из контрактов и
    проче инфы (заказчик, штрафы,)
    '''
    # НУЖНО ОТФИЛЬТРОВАТЬ УЖЕ ОТПАРСЕННЫЕ КОНТРАКТЫ
    # получение инфы из связи контракт - продукт
    # вызывает новое обращение к бд - очень долго
    # получаем номера отпарсенных контракты
    p_numbers = set(self.Product.query.with_entities(self.Product.contrant_card_id).all())
    # получаем номера всех контракты
    c_numbers = set(self.Contrant_card.query.with_entities(self.Contrant_card.number).all())
    # оставляем номера только тех, которые не парсили
    not_parsed_numbers_set = c_numbers - p_numbers
    # !!! ВОЗВРАЩАЕТ { (1780100227424000036,), (3890505754424000005,), ...}
    print(len(not_parsed_numbers_set))

    # print(not_parsed_numbers_set)

    p_counter = 0
    for contruct_number in not_parsed_numbers_set:
        p_counter += 1
        self.get_product_page(contruct_number[0])
        if p_counter > 1:
            break


Parser_ver_2.parse_products = parse_products
Parser_ver_2.get_product_page = get_product_page
