from zakupki.db.models import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from typing import Optional
import datetime
import json

def get_ktru_by_number(session, number: str) -> Optional[Ktru]:
    return session.execute(select(Ktru).where(Ktru.number == number)).scalar_one_or_none()

def create_ktru(session, ktru_data: dict):
    """
    Создаёт запись Ktru в переданной SQLAlchemy сессии.
    Ожидаемые ключи в ktru_data:
      - number (str) обязательное, уникальное
      - name (str) опционально
      - unit (str) опционально
      - ownCharsIsForbidden (bool) опционально
    Возвращает объект Ktru (не обязательно скоммиченный).
    Бросает ValueError при некорректных данных или IntegrityError при нарушении ограничений БД.
    """

    number = ktru_data.get("number")

    # Дополнительные поля
    name = ktru_data.get("name")
    unit = ktru_data.get("unit")
    own_forbidden = ktru_data.get("ownCharsIsForbidden")

    # Создаём объект
    new_ktru = Ktru(
        number=str(number),
        name=str(name) if name is not None else None,
        unit=str(unit) if unit is not None else None,
        ownCharsIsForbidden=bool(own_forbidden) if own_forbidden is not None else False,
    )

    try:
        session.add(new_ktru)
        session.flush()  # получить id и проверить целостность до внешнего commit
    except IntegrityError:
        session.rollback()
        raise

    # можно вернуть объект; вызывающий код должен делать commit через session_scope()
    return new_ktru

def get_user_version_for_ktru(session, ktru_obj: Ktru, user_version: int) -> Optional[KtruVersion]:
    # ищем определенную версию для данного ktru
    u_version = (
        session.query(KtruVersion)
        .filter(KtruVersion.ktruId == ktru_obj.id,
        KtruVersion.versionNumber == user_version)
        .first()
    )
    return u_version  # вернёт объект KtruVersion или None

def get_latest_version_for_ktru(session, ktru_obj: Ktru) -> Optional[KtruVersion]:
    # Получаем все версии для данного ktru и выбираем максимальную по versionNumber
    latest = (
        session.query(KtruVersion)
        .filter(KtruVersion.ktruId == ktru_obj.id)
        .order_by(KtruVersion.versionNumber.desc())
        .first()
    )
    return latest  # вернёт объект KtruVersion или None

def create_ktru_version(session, ktru_id, version_number, date_update=None):
    # Создаём объект
    new_version_number = KtruVersion(
        ktruId=ktru_id,
        versionNumber=version_number,
        dateUpdate=date_update
    )
    try:
        session.add(new_version_number)
        session.flush()  # получить id и проверить целостность до внешнего commit
    except IntegrityError:
        session.rollback()
        raise

    # можно вернуть объект; вызывающий код должен делать commit через session_scope()
    return new_version_number

def get_chars_for_version(session, ktru_version_obj: KtruVersion) -> list[KtruChars]:
    chars = (
        session.query(KtruChars)
        .filter(KtruChars.ktruVersionId == ktru_version_obj.id)
        .all()
    )
    return chars

def create_ktru_chars_bulk(session, ktru_version_obj, chars_list):
    """
    chars_list — список словарей с ключами:
      "charName" (str), "isRequired" (bool/ignored), "unit" (str|None), "values" (list[str])

    Использует bulk_insert_mappings для массовой вставки.
    """
    if not chars_list:
        return []

    ktru_version_id = ktru_version_obj.id
    if ktru_version_id is None:
        raise ValueError("ktru_version_obj.id is None — объект должен быть сохранён в БД")

    mappings = []
    for ch in chars_list:
        # Валидация/нормализация входа
        name = ch.get("charName") or ch.get("name")
        values = ch.get("values", [])
        unit = ch.get("unit")
        isRequired = ch.get("isRequired")
        if name is None:
            raise ValueError("Каждый элемент chars_list должен содержать 'charName'")

        # Сериализуем values в JSON строку
        values_json = json.dumps(values, ensure_ascii=False)

        mappings.append({
            "ktruVersionId": ktru_version_id,
            "name": name,
            "values": values_json,
            "unit": unit,
            "isRequired": isRequired,
        })

    try:
        # bulk insert
        session.bulk_insert_mappings(KtruChars, mappings)
        session.flush()  # чтобы получить присвоенные id, если нужно
    except SQLAlchemyError:
        session.rollback()
        raise

    # Если нужно вернуть ORM-объекты, можно заново запросить их из БД
    inserted = (
        session.query(KtruChars)
        .filter(KtruChars.ktruVersionId == ktru_version_id)
        .all()
    )
    return inserted

def create_ktru_chars_bulk_orm(session, ktru_version_obj, chars_list):
    created = []
    for ch in chars_list:
        obj = KtruChars(
            ktruVersionId=ktru_version_obj.id,
            name=ch.get("charName"),
            values=json.dumps(ch.get("values", []), ensure_ascii=False),
            unit=ch.get("unit")
        )
        ktru_version_obj.chars.append(obj)  # сессия отслеживает изменения
        created.append(obj)
    session.flush()
    return created

def log_request(session, request_name, is_success, ktru_number, ktru_version):
    new_request = Requests(
        requestName=request_name,
        isSuccess=is_success,
        ktruNumber=ktru_number,
        ktruVersion=ktru_version,
        date=datetime.datetime.utcnow()
    )
    session.add(new_request)

def get_request(session, request_name, ktru_number:str, current_date:datetime, version=None):
    result = session.query(Requests).filter(
        Requests.requestName == request_name,
        Requests.ktruNumber == ktru_number,
        Requests.date >= current_date,
    )
    if version:
        result = result.filter(Requests.ktruVersion == version)

    result = result.order_by(Requests.date.desc()).first()

    return result
