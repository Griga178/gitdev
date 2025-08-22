
# Импорты
import datetime
from contextlib import contextmanager
from typing import List, Optional, Dict, Any

from sqlalchemy import create_engine, select, func, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from get_ktru_chars import get_html_content
from get_ktru_chars import parse_ktru_chars_table_from_html
from get_ktru_params import get_last_ktru_version
from get_ktru_params import get_common_data

from models import *
import settings
# Подключите ваши модели: Ktru, KtruVersion, KtruChars, Requests
# Пример: from models import Ktru, KtruVersion, KtruChars, Requests

# Настройка engine/session (подставьте вашу строку подключения)
engine = create_engine(settings.db_path, echo=False, future=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def utc_now() -> datetime.datetime:
    return datetime.datetime.utcnow()

def today_utc_date() -> datetime.date:
    return utc_now().date()

def log_request(session, request_name: str, is_success: bool, ktru_number: str,
                ktru_version: Optional[int] = None, error_message: Optional[str] = None):
    """
    Добавляет запись в Requests (без commit).
    Ожидается, что модель Requests имеет хотя бы поля:
    requestName, isSuccess (bool), ktruNumber, ktruVersion (nullable), date (datetime), errorMessage (nullable)
    """
    req = Requests(
        requestName=request_name,
        isSuccess=bool(is_success),
        ktruNumber=ktru_number,
        ktruVersion=ktru_version,
        date=utc_now()
    )
    session.add(req)

def had_successful_f2_today(session, ktru_number: str) -> bool:
    """
    Проверяет, был ли сегодня успешный вызов f2 для данного номера в таблице Requests.
    """
    today_start = datetime.datetime.combine(today_utc_date(), datetime.time.min)
    today_end = datetime.datetime.combine(today_utc_date(), datetime.time.max)
    q = select(func.count()).where(
        and_(
            Requests.requestName == "f2",
            Requests.isSuccess == True,
            Requests.ktruNumber == ktru_number,
            Requests.date >= today_start,
            Requests.date <= today_end
        )
    )
    cnt = session.execute(q).scalar_one()
    return cnt > 0

def get_latest_version_from_db(session, ktru_id: int) -> Optional[KtruVersion]:
    return session.execute(
        select(KtruVersion)
        .where(KtruVersion.ktruId == ktru_id)
        .order_by(KtruVersion.versionNumber.desc())
    ).scalars().first()

def get_chars_for_version(session, ktru_version_id: int) -> List[Dict[str, Any]]:
    rows = session.execute(
        select(KtruChars).where(KtruChars.ktruVersionId == ktru_version_id)
    ).scalars().all()
    result = []
    for r in rows:
        result.append({
            "name": r.name,
            "values": r.values,
            "unit": r.unit
        })
    return result

def handle_number(x_num: str, f1, f2, f3) -> List[Dict[str, Any]]:
    """
    f1(num) -> dict (общие данные)
    f2(num) -> int (версияNumber)
    f3(num, version) -> list[dict] (характеристики)
    Возвращает список характеристик.
    """
    with session_scope() as session:
        stage = "# 1. Получаем или создаём Ktru"
        print(stage)
        with session.begin_nested():
            ktru = session.execute(select(Ktru).where(Ktru.number == x_num)).scalars().first()
            if ktru is None:
                print("## В БД КТРУ - нет")
                try:
                    data = f1(x_num)
                except Exception as e:
                    log_request(session, "f1", False, x_num, None, error_message=str(e))
                    raise
                if not isinstance(data, dict):
                    log_request(session, "f1", False, x_num, None, error_message="f1 returned non-dict")
                    raise ValueError("f1 returned non-dict")
                ktru = Ktru(
                    number=x_num,
                    name=data.get("name"),
                    unit=data.get("unit"),
                    ownCharsIsForbidden=bool(data.get("ownCharsIsForbidden", False))
                )
                print("## Отпарсили:", ktru.__dict__)
                session.add(ktru)
                session.flush()
                log_request(session, "f1", True, x_num, None)

        stage = "# 2. Решаем, вызывать ли f2: если сегодня уже был успешный f2 — не вызывать."
        print(stage)
        with session.begin_nested():
            version_number: Optional[int] = None
            version_obj: Optional[KtruVersion] = None

            if had_successful_f2_today(session, x_num):
                # Берём последнюю версию из БД (если есть)
                version_obj = get_latest_version_from_db(session, ktru.id)
                if version_obj:
                    version_number = version_obj.versionNumber
                # Если version_obj отсутствует, всё равно нужно вызвать f2, т.к. нет данных в KtruVersion
            else:
                # Никакого успешного f2 сегодня — вызываем f2
                try:
                    v = f2(x_num)
                except Exception as e:
                    log_request(session, "f2", False, x_num, None, error_message=str(e))
                    raise
                if not isinstance(v, int):
                    print(v)
                    log_request(session, "f2", False, x_num, None, error_message="f2 returned non-int")
                    raise ValueError("f2 returned non-int")
                version_number = v
                # логируем успешный f2
                log_request(session, "f2", True, x_num, version_number)

                # убедимся, что в KtruVersion есть запись для этой версии
                existing = session.execute(
                    select(KtruVersion)
                    .where(and_(KtruVersion.ktruId == ktru.id, KtruVersion.versionNumber == version_number))
                ).scalars().first()
                if existing:
                    version_obj = existing
                else:
                    version_obj = KtruVersion(
                        ktruId=ktru.id,
                        versionNumber=version_number,
                        dateUpdate=utc_now()  # сюд�� можно подставить дату, если f2 возвращает её отдельно
                    )
                    session.add(version_obj)
                    session.flush()

        stage = "# 3. Если у нас есть version_obj, проверяем характеристики в БД"
        print(stage)
        with session.begin_nested():
            if version_obj:
                chars_in_db = get_chars_for_version(session, version_obj.id)
                if chars_in_db:
                    return chars_in_db

        stage = "# 4. Если характеристик нет — вызываем f3"
        print(stage)
        with session.begin_nested():
            if version_number is None:
                # Если нет version_number (редкий кейс), пытаемся получить из последней версии в DB
                if version_obj:
                    version_number = version_obj.versionNumber
                else:
                    # нет версии и не получилось получить — вызываем f2 принудительно
                    try:
                        v = f2(x_num)
                    except Exception as e:
                        log_request(session, "f2", False, x_num, None, error_message=str(e))
                        raise
                    if not isinstance(v, int):
                        log_request(session, "f2", False, x_num, None, error_message="f2 returned non-int")
                        raise ValueError("f2 returned non-int")
                    version_number = v
                    log_request(session, "f2", True, x_num, version_number)
                    existing = session.execute(
                        select(KtruVersion)
                        .where(and_(KtruVersion.ktruId == ktru.id, KtruVersion.versionNumber == version_number))
                    ).scalars().first()
                    if existing:
                        version_obj = existing
                    else:
                        version_obj = KtruVersion(ktruId=ktru.id, versionNumber=version_number, dateUpdate=utc_now())
                        session.add(version_obj)
                        session.flush()

        stage = '# Вызов f3'
        print(stage)
        with session.begin_nested():
            try:
                chars = f3(x_num, version_number)
            except Exception as e:
                log_request(session, "f3", False, x_num, version_number, error_message=str(e))
                raise
            if not isinstance(chars, list):
                log_request(session, "f3", False, x_num, version_number, error_message="f3 returned non-list")
                raise ValueError("f3 returned non-list")

        # Сохраняем характеристики в БД
        if not version_obj:
            version_obj = KtruVersion(ktruId=ktru.id, versionNumber=version_number, dateUpdate=utc_now())
            session.add(version_obj)
            session.flush()

        for ch in chars:
            kc = KtruChars(
                ktruVersionId=version_obj.id,
                name=ch.get("name"),
                values=ch.get("values"),
                unit=ch.get("unit")
            )
            session.add(kc)

        log_request(session, "f3", True, x_num, version_number)
        return chars

# Пример stub-функций и вызова (для тестирования)

if __name__ == "__main__":
    valid_ktru_number = '26.20.17.110-00000037'
    def f1_stub(num):
        url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-description.html?itemId={num}'
        html_content = get_html_content(url)
        return get_common_data(html_content)
    def f2_stub(num):
        url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/version-journal.html?itemId={num}'
        html_content = get_html_content(url)
        return get_last_ktru_version(html_content)
    def f3_stub(num, ver):
        url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-part-description.html?itemVersionId={num}_{ver}&page=1&recordsPerPage=1000&isTemplate=false&onlyRequired=false'
        html_content = get_html_content(url)
        return parse_ktru_chars_table_from_html(html_content)

    print(handle_number(valid_ktru_number, f1_stub, f2_stub, f3_stub))
