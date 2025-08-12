import requests
from bs4 import BeautifulSoup
from typing import Optional

from get_ktru_params import get_last_ktru_version
from models import *
import settings

class KTRUManager:
    '''
        если парсинг не удался, есть возможность повторить позже, в БД requests
        сохраняется инфа по запросам
    '''
    def __init__(self, db_path=settings.db_path):
        self.db_path = db_path
        self.session_maker = self._init_db()
        # self.session = self.session_maker()
        self.get_last_ktru_version = get_last_ktru_version

    def _init_db(self):
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine)

    def _load_ktru_version_if_exists(self, ktru_number: str, version_number: int) -> bool:
        """
        Проверяет наличие версии КТРУ с определённым номером версии.

        :param ktru_number: номер КТРУ
        :param version_number: номер версии
        :return: KtruVersion() - если версия есть, False - если нет
        """
        with self.session_maker() as session:
            # Получаем КТРУ по номеру
            ktru_obj = session.query(Ktru).filter(Ktru.number == ktru_number).first()
            if not ktru_obj:
                return False

            # Ищем версию с нужным номером
            version = session.query(KtruVersion).filter(
                KtruVersion.ktruId == ktru_obj.id,
                KtruVersion.versionNumber == version_number
            ).first()
            if version:
                return version
            else:
                return False

    def _save_to_db(self, ktru_number, data):
        pass

    def _load_ktru_if_exists(self, ktru_number: str):

        with self.session_maker() as session:
            # Получаем КТРУ по номеру
            ktru_obj = session.query(Ktru).filter(Ktru.number == ktru_number).first()
            if not ktru_obj:
                return False
            else:
                return ktru_obj

    def get_ktru_info(self, ktru_number:str, ktru_version_number:int=None) -> list[KtruVersion,...]:
        # инфа откуда будет информация
        # None - запроса не было
        # True - инфа с сайта
        # False - инфа из БД (какая есть), запрос не удачный
        data = {'request': None }
        msg = f'Запрос КТРУ: "{ktru_number}" версия: "{str(ktru_version_number)}"'
        print(msg)
        if ktru_version_number:
            print(" - Указана версия КТРУ")
            # пробуем загрузить из БД
            ktru_version = self._load_ktru_version_if_exists(ktru_number, ktru_version_number)
            if ktru_version:

                if ktru_version.chars:
                    return ktru_version.chars
                else:
                    # парсим характеристики
                    pass
            else:
                print(' -  - В БД нет записи о версии КТРУ')
                # смотрим есть ли ktru_number в БД
                ktru = self._load_ktru_if_exists(ktru_number)
                if ktru:
                    # создаем requests
                    # парсим характеристики
                    pass
                else:
                    print(' -  - В БД нет записи о КТРУ')
                    # создаем requests
                    # парсим общие данные
                    # парсим характеристики
                    pass
        else: # пользователь не укзывает версию ктру
            print(" - версия КТРУ не указана")
            # смотрим есть ли ktru_number в БД
            ktru = self._load_ktru_if_exists(ktru_number)
            if ktru:
                print(' -  - Номер КТРУ есть в БД')
                # создаем requests
                # парсим номер последней версии
                # ktru_version_number = self.get_last_ktru_version()
                if ktru_version_number:
                    '''
                        НУЖНО ПРОВЕРИТЬ
                    '''
                    if ktru_version_number == ktru.versions[-1].versionNumber:
                        if ktru.versions[-1].chars:
                            return ktru.versions[-1].chars
                        else:
                            # парсим характеристики последней версии
                            pass

                    else:
                        # парсим характеристики последней версии
                        pass
                else:
                    # парсим характеристики последней версии
                    pass
            else:
                print(' -  - В БД нет номера КТРУ')
                # создаем requests
                # парсим номер последней версии
                version_number = self._parse_last_version_number(ktru_number)
                # парсим общие данные
                # парсим характеристики
                pass

        return data

    def _fetch_from_site(self, url):

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на успешность запроса
            return response.text
        except requests.RequestException as e:
            return f"Ошибка при получении страницы: {e}"

    def _parse_last_version_number(self, ktruNumber:str) -> Optional[int, None]:
        request_params = {'requestName': "version", "ktruNumber": ktruNumber}
        request = _load_requests(**request_params)
        if request:
            # если есть неудачный рек. - повторяем
            pass
        url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/version-journal.html?itemId={ktruNumber}'
        soup = BeautifulSoup(html_content, 'html.parser')

        return self.get_last_ktru_version(soup)

    def update_all_ktru(self):
        pass

    def update_requests(self):
        # загрузить все requests где isSuccess = False
        if request_name = "version":
            # парсим последнюю версию КТРУ
            # проверяем есть ли requests с "ktru_chars" по КТРУ и Версии
            pass
        elif request_name = "ktru_info":
            # парсим общую инфу по КТРУ
            pass
        elif request_name = "ktru_chars":
            pass
