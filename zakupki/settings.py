# Даты поиска контрактов
START_DATE = '27/02/2023'

END_DATE = '16/10/2023' # default = .now()
# END_DATE = False

DAYS_STEP = 5 # ИСКАТЬ КОНТРАКТЫ ЗА X ДНЕЙ

# Путь до актуального драйвера для "Яндекса"
selenium_driver = '../yandexdriver.exe'

# Имя и место хранение SQL Базы данных
SQL_FILE_NAME = 'zakupki_contracts.db'

DATA_BASE_PATH = f'sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/{SQL_FILE_NAME}'


def get_last_conrtact():
    '''
        ЧТО БЫ УСТАНОВИТЬ ДАТУ СТАРТА
        = ПОСЛЕДНЕЕ - 5 ДНЕЙ
    '''
    from database import Data_base_API
    DB_API = Data_base_API(DATA_BASE_PATH)

    all_contracts = DB_API.contrant_cards.select()
    all_contracts.sort(key = lambda x: x.date)
    print('Всего контрактов:', len(all_contracts))
    print('Всего контрактов:', all_contracts[-1])

# get_last_conrtact()
