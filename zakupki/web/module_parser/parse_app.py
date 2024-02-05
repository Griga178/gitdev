import time
from datetime import datetime
from .driver_setting import get_driver
from .gov_set_filter import setup_site_filter
from .date_list_set import get_days
from .parse_func_last_date import get_last_conrtact_date

class Parse_app():
    def __init__(self, app, Contrant_card):
        self.Contrant_card = Contrant_card
        self.app = app

        self.is_active = 0
        self.str_status = 'Остановлен'
        self.counter = 0
        self.start_counter = 0
        self.stop_counter = 0
        self.max_time = 1000
        print('Создан экземпляр "Парсера"')

        self.parse_date_from = False
        self.parse_date_to = False
        self.start_date = get_last_conrtact_date(self)
        self.end_date = datetime.now()
        self.list_date = False # Спиок дат для парсинга
        self.day_index = 0 # Индекс даты, которую парсим
        self.DAYS_STEP = 5 # перид филтрации контрактов в днях
        self.contract_amount = 0
        self.parse_progress = 0

    def parse_numbers(self, **kwargs):

        self.is_active = 1
        self.str_status = 'Запуск браузера'

        # запуск браузера
        self.get_driver = get_driver()
        # настройка первичных фильтрв
        self.str_status = 'Настройка фильтра гос услуг'
        setup_site_filter(self.get_driver)
        # поиск контрактов по датам

        step = self.DAYS_STEP

        while self.day_index < len(self.list_date) and self.is_active == 1:
            pre_index = self.day_index # что бы переписать даты
            day_from = self.list_date[self.day_index]
            self.day_index += step
            if self.day_index >= len(self.list_date):
                self.day_index = len(self.list_date) - 1
            day_to =  self.list_date[self.day_index]
            self.day_index += 1
            period = self.day_index - pre_index
            # вставляем даты в поисковик
            self.parse_date_from = day_from
            self.parse_date_to = day_to
            ''' parsing '''
            # print(self.day_index, len(self.list_date))
            self.parse_progress = round(self.day_index / (len(self.list_date))*100)
            time.sleep(0.5)
            print(self.parse_progress)

        else:
            self.is_active = 0
            self.get_driver.close()

    def refresh_app(self):
        self.start_date = get_last_conrtact_date(self)
        self.contract_amount = 0
        self.parse_progress = 0
        self.day_index = 0

    def set_dates(self, **kwargs):
        try:
            if kwargs.get('start_date'):
                self.start_date = datetime.strptime(kwargs['start_date'], "%Y-%m-%d")
            else:
                self.start_date = get_last_conrtact_date(self)
        except:
            if kwargs.get('start_date'):
                return 'error message'
            else:
                self.start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")

        if kwargs.get('end_date'):
            self.end_date = datetime.strptime(kwargs['end_date'], "%Y-%m-%d")
        else:
            self.end_date = datetime.now()

        self.list_date = get_days(self.start_date, self.end_date)

        return True
    def get_info(self):

        return {
            'is_active': self.is_active,
            'str_status': self.str_status,
            'counter': self.counter,
            'start_counter': self.start_counter,
            'stop_counter': self.stop_counter,
            'parse_progress': self.parse_progress,

            'start_date': self.start_date,
            'end_date': self.end_date,
            'parse_date_from': self.parse_date_from,
            'parse_date_to': self.parse_date_to,
        }
