import time
from .driver_setting import get_driver

class Parse_app():
    def __init__(self):
        self.is_active = False
        self.counter = 0
        self.start_counter = 0
        self.stop_counter = 0
        self.max_time = 1000
        print('Создан экземпляр "Парсера"')

        self.parse_date = False
        self.start_date = False
        self.end_date = False

        self.contract_amount = 0

    def run_app(self):
        self.is_active = True
        self.start_counter += 1
        print(f"Start app {self.start_counter}")
        self.main_procces()

    def parse_numbers(self, **kwargs):
        self.is_active = False
        self.set_dates(**kwargs)
        # запуск браузера
        self.get_driver = ''
        # настройка первичных фильтрв
        # self.set_filters()
        # поиск контрактов по датам
        # while True:
        #     pass


    def set_dates(self, **kwargs):
        if kwargs.get('start_date'):
            self.start_date = kwargs['start_date']
        else:
            # self.start_date = self.get_last_contract_date()
            self.start_date = 'last db date'

        if kwargs.get('end_date'):
            self.end_date = kwargs['end_date']
        else:
            self.end_date = 'now'

    def main_procces(self):

        while self.is_active and self.max_time > self.counter:
            self.counter += 1
            # print(f'{self.counter} - step')
            time.sleep(0.1)

    def stop_app(self):
        self.is_active = False
        self.stop_counter += 1
        print(f"Stop app {self.stop_counter}")

        return self.get_info()

    def get_info(self):

        return {
            'is_active': self.is_active,
            'counter': self.counter,
            'start_counter': self.start_counter,
            'stop_counter': self.stop_counter,

            'start_date': self.start_date,
            'end_date': self.end_date,
            'parse_date': self.parse_date
        }
