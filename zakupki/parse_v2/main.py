import requests

from .bs_funcs import *
from .convert_data import *

class Parser_ver_2():
    def __init__(self, app, Contrant_card):
        self.url = 'https://zakupki.gov.ru/epz/contract/search/results.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            }
        self.params = {
            'morphology': 'on',
            'search-filter': 'Цене', # 'Цене' 'Дате размещения'
            'fz44': 'on',
            'contractStageList_1': 'on',
            'contractStageList': 1,
            'contractCurrencyID': -1,
            'budgetLevelsIdNameHidden': '{}',
            # 'contractDateFrom': '30.12.2023',
            # 'contractDateTo': '02.02.2024',
            'sortBy': 'PRICE', #PRICE UPDATE_DATE
            'pageNumber': 1, # '1'
            'sortDirection': 'false',
            'recordsPerPage': '_50', #_10, _20, _50
            'showLotsInfoHidden': 'false',
            'customerPlace': 5277347,
            'customerPlaceCodes': 78000000000
            }

        self.is_active = False
        self.str_status = 'Остановлен'
        self.counter = 0
        self.parse_progress = 0
        self.days_amount = 0
        self.session = requests.Session()
        self.query_attemps_q = 0
        self.report = {}
        self.date_from = False
        self.date_to = False
        self.filter_date_from = False
        self.filter_date_to = False
        self.price_filter = False

        response = self.session.get(
            self.url,
            headers = self.headers)

        if response.status_code != 200:
            print(response)

            return {'error': 1,
            'message': f'Ошибка {response.status_code} при запуске'}
        else:
            self.status_code = response.status_code

    def get_query(self):
        response = self.session.get(
            self.url,
            headers = self.headers,
            params = self.params)
        return response

    def set_dates(self, *args, **kwargs):
        if len(args) == 1:
            self.date_from = string_to_datetime(args[0])
        elif len(args) == 2:
            self.date_from = string_to_datetime(args[0])
            self.date_to = string_to_datetime(args[1])
        else:

            if kwargs.get('date_from') or kwargs.get('date_to'):
                self.date_from = string_to_datetime(kwargs.get('date_from')) if kwargs.get('date_from') else False
                self.date_to = string_to_datetime(kwargs.get('date_to')) if kwargs.get('date_to') else False
            else:
                pass
                print(f'Не вставлены даты a:{args} k:{kwargs}')

        if self.date_to == False:
            self.date_to = datetime.now()
            self.date_to = self.date_to - timedelta(
                    hours = self.date_to.hour,
                    minutes = self.date_to.minute,
                    seconds = self.date_to.second,
                    microseconds = self.date_to.microsecond)

        # last_datetime = get_last_conrtact_date(self) # последний отпарсенный контракт
        if self.date_from == False:
            self.date_from = string_to_datetime('01/01/2022')

        self.filter_date_from = self.date_from
        # else:
        #     if last_datetime > self.date_from:
        #         self.date_from = last_datetime

    def set_dates_query(self):
        self.params['contractDateFrom'] = self.filter_date_from.strftime('%d.%m.%Y')
        self.params['contractDateTo'] = self.filter_date_to.strftime('%d.%m.%Y')

    def parse_contract_numbers(self):
        self.is_active = True
        self.str_status = 'Запущен'
        self.days_amount = (self.date_to - self.date_from).days
        days_step = 5
        # настраиваем запрос
        self.filter_date_to = self.filter_date_from + timedelta(days = days_step)
        self.set_dates_query()
        print('Запуск парсера')
        while self.filter_date_from < self.date_to:
            self.parse_progress = round((self.date_to - self.filter_date_from).days / self.days_amount)*100)
            response = self.get_query()
            if response.status_code != 200:
                print(f'ОШИБКА ПРИ ПЕРВОМ ЗАПРОСЕ: {response.status_code} ({self.query_attemps_q})')
                if self.query_attemps_q > 10:
                    self.report['message'] = f'>10 попыток запроса {response.status_code}'
                    self.report.update(self.params)
                    print(self.report)
                    break
                time.sleep(1)
                self.query_attemps_q += 1
                continue
            else:
                self.query_attemps_q = 0
            # проверяем количество контрактов
            contract_amount = get_contract_amount(response)
            print(self.params['contractDateFrom'], '-', self.params['contractDateTo'])
            print('Нашлось контрактов:', contract_amount)

            if contract_amount == 0:
                self.filter_date_from += timedelta(days = 1)
                self.filter_date_to = self.filter_date_from + timedelta(days = days_step)
                self.set_dates_query()
                continue
            elif contract_amount < 1000:
                page_amount = get_page_amount(contract_amount)
                self.price_filter = False
            else:

                if self.filter_date_from == self.filter_date_to:
                    page_amount = 20
                    self.price_filter = True
                else:
                    self.filter_date_to = self.filter_date_to - timedelta(days = 1)
                    self.set_dates_query()
                    continue

            # сохраняем контракты - перелистываем
            contrant_cards = []
            for i in range(page_amount):
                print(f'скачиваем контракты с листа № {self.params["pageNumber"]}')
                contrant_cards += get_contract_numbers(response)
                print('перелистываем')
                self.params['pageNumber'] += 1

                response = self.get_query()
                if response.status_code != 200:
                    print(f'ОШИБКА ПРИ ПЕРЕЛИСТЫВАНИИ: {response.status_code} ({self.query_attemps_q})')
                    if self.query_attemps_q > 10:
                        self.query_attemps_q = 0
                        self.report['message'] = f'>10 попыток запроса ПЕРЕЛИСТЫВАНИЯ {response.status_code}'
                        self.report.update(self.params)
                        print(self.report)
                        if contrant_cards:
                            print(f'Контракты сохранили {len(contrant_cards)}')

                        break
                    time.sleep(1)
                    self.query_attemps_q += 1
                    continue
                else:
                    self.query_attemps_q = 0

            else:
                self.params['pageNumber'] = 1
                print(f'Контракты сохранили {len(contrant_cards)}')

            if self.price_filter:
                # максимальная цена отпарсенного контракта
                self.params['contractPriceFrom'] = 1000000
            else:
                self.filter_date_from = self.filter_date_to + timedelta(days = 1)
                self.filter_date_to += timedelta(days = days_step)
                self.set_dates_query()
                if self.params.get('contractPriceFrom'):
                    del self.params['contractPriceFrom']
        else:
            self.str_status = 'Остановлен'
            self.is_active = False
            self.parse_progress = 100
            # self.params['pageNumber'] = 1
            if self.params.get('contractPriceFrom'):
                del self.params['contractPriceFrom']
            # if self.params.get('contractDateFrom'):
            #     del self.params['contractDateFrom']
            # if self.params.get('contractDateTo'):
            #     del self.params['contractDateTo']


    def get_info(self):

        return {
            'is_active': self.is_active,
            'str_status': self.str_status,
            'counter': self.counter,
            # 'start_counter': self.start_counter,
            # 'stop_counter': self.stop_counter,
            'parse_progress': self.parse_progress,

            'start_date': self.date_from,
            'end_date': self.date_to,
            'parse_date_from': self.filter_date_from,
            'parse_date_to': self.filter_date_to,
        }
