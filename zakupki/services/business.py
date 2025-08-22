# services/business.py
from typing import Tuple, Optional, Dict, List
import datetime
import logging
import json

from zakupki.z_parser.fetcher import get_html_content
from zakupki.z_parser.extractor import (
    parse_common_data,
    parse_ktru_version,
    parse_ktru_chars_table_from_html,
)
from zakupki.db.client import session_scope
import zakupki.db.queries as queries
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class BusinessError(Exception):
    pass

import json
from typing import List, Dict


def print_stage(msg: dict, print_stage_on: bool):
    if not print_stage_on:
        return

    ktru_number = msg.get(1)
    info_status = msg.get(2)
    version_status = msg.get(3)
    chars_status = msg.get(4)
    ktru_name = msg.get(5)
    # empt_r = ' '.join(['' for i in range(90)])
    # print('\r\033[K', end='')
    # print(empt_r, end='\r')
    row = ""
    if ktru_number:
        # print(ktru_number.center(24), end=' |')
        row += ktru_number.center(21) + "|"
    if info_status:
        # print(info_status.center(15), end=' |')
        row += info_status.center(21) + "|"
    if version_status:
        # print(version_status.center(15), end=' |')
        row += version_status.center(21) + "|"
    if chars_status:
        if chars_status[-1] == "*":
            row += chars_status.center(21) + "|"
            # print(chars_status.center(15), end=' |\n')
            # disp = ['-- ' for i in range(30)]
            # print(''.join(disp))
        else:
            # print(chars_status.center(15), end=' |')
            row += chars_status.center(21) + "|"
            # print(' ')
    print(row, end = '\r')
    if ktru_name:
        row += ktru_name
        print(row.ljust(4))


def ktru_chars_to_dicts(chars: List[object]) -> List[Dict]:
    """
    Преобразует список объектов KtruChars в список словарей.
    Ожидается, что attrs объектов:
      id, ktruVersionId, name, values (JSON-строка или уже list), unit, isRequired
    Если values пустое или некорректное - приводим к пустому списку.
    """
    result = []
    for obj in chars:
        # безопасно взять атрибуты
        _id = getattr(obj, "id", None)
        _ktruVersionId = getattr(obj, "ktruVersionId", None)
        _name = getattr(obj, "name", None)
        raw_values = getattr(obj, "values", None)
        _unit = getattr(obj, "unit", None)
        _isRequired = getattr(obj, "isRequired", None)

        # обработка values: если уже список — оставить, если строка — попытаться распарсить JSON
        parsed_values = []
        if isinstance(raw_values, list):
            parsed_values = raw_values
        elif isinstance(raw_values, str):
            raw_values_str = raw_values.strip()
            if raw_values_str:
                try:
                    parsed = json.loads(raw_values_str)
                    # ожидаем список, иначе превращаем в список из единственного элемента
                    parsed_values = parsed if isinstance(parsed, list) else [parsed]
                except json.JSONDecodeError:
                    # попытка простого разделения по запятым как запасной вариант
                    parsed_values = [v.strip() for v in raw_values_str.split(",") if v.strip()]
        else:
            parsed_values = []

        result.append({
            "id": _id,
            "ktruVersionId": _ktruVersionId,
            "name": _name,
            "values": parsed_values,
            "unit": _unit,
            "isRequired": _isRequired
        })
    return result


def fetch_for_parse_version(session, ktru_number):
    url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/version-journal.html?itemId={ktru_number}'
    request_name = "version"
    html, fetch_error = get_html_content(url)
    if fetch_error:
        with session.begin_nested():
            # логируем неуспешный запрос в БД минимально (если возможно)
            try:
                queries.log_request(session, request_name, False, ktru_number or "", None)
            except Exception:
                logger.exception("Failed to log failed request")
            raise BusinessError(f"Fetch failed: {fetch_error}")
    return html


def fetch_for_parse_ktru(session, ktru_number):
    url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-description.html?itemId={ktru_number}'
    # url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-description.html?itemId=58.29.32.000-00000001'
    request_name = "ktru_info"
    html, fetch_error = get_html_content(url)
    if fetch_error:
        # логируем неуспешный запрос в БД минимально (если возможно)
        with session.begin_nested():
            try:
                queries.log_request(session, request_name, False, ktru_number or "", None)
            except Exception:
                logger.exception("Failed to log failed request")
            raise BusinessError(f"Fetch failed: {fetch_error}")
    return html


def fetch_for_pasrse_chars(session, ktru_number, version):
    url = f'https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-part-description.html?itemVersionId={ktru_number}_{version}&page=1&recordsPerPage=1000&isTemplate=false&onlyRequired=false'
    request_name = "ktru_chars"
    html, fetch_error = get_html_content(url)
    if fetch_error:
        # логируем неуспешный запрос в БД минимально (если возможно)
        with session.begin_nested():
            try:
                queries.log_request(session, request_name, False, ktru_number or "", None)
            except Exception:
                logger.exception("Failed to log failed request")
            raise BusinessError(f"Fetch failed: {fetch_error}")
    return html


def fetch_parse_and_store_ktru(ktru_number: str, user_version:Optional[int] = None, print_stage_on = True) -> Dict[str, Optional[object]]:
    """
    Основная функция: получает HTML, парсит общие данные, версию и характеристики,
    синхронизирует с БД. Возвращает словарь с результатом.

    version: Опционально, если указана версия выдаем ее иначе, последнюю

    print_stage_on: bool -если True - выводит результаты в консоль
    """
    # Начинаем работу с БД
    msg = {}
    try:
        with session_scope() as session:
            # 1. Получаем или создаём Ktru
            msg[1] = ktru_number
            msg[2] = "info - check DB..."
            print_stage(msg, print_stage_on)

            ktru = queries.get_ktru_by_number(session, ktru_number)
            if ktru:
                msg[2] = "info - DB" if ktru else ""
                print_stage(msg, print_stage_on)
            else:
                msg[2] = "DB-None info - fetching..."
                print_stage(msg, print_stage_on)
                html = fetch_for_parse_ktru(session, ktru_number)
                # Парсим общие данные
                common = parse_common_data(html)
                msg[2] = "DB-None info - parsing..."
                print_stage(msg, print_stage_on)

                # Ожидается, что parse_common_data вернёт словарь с ключами:
                # number, name, unit, ownCharsIsForbidden (как минимум)
                number = ktru_number or common.get("number")
                if not number:
                    raise BusinessError("KTRU number not found in parsed common data")
                ktru_payload = {
                    "number": number,
                    "name": common.get("name"),
                    "unit": common.get("unit"),
                    "ownCharsIsForbidden": common.get("ownCharsIsForbidden"),
                }
                with session.begin_nested():
                    ktru = queries.create_ktru(session, ktru_payload)
                    logger.info("Created new Ktru number=%s id=%s", number, getattr(ktru, "id", None))

                msg[2] = "info - Parsed"
                print_stage(msg, print_stage_on)

            # 2. получение версии
            msg[3] = "version - chek requests..."
            print_stage(msg, print_stage_on)

            db_failed_request_exist = False
            need_new_parse = False
            # срок годности запросов 1месяц
            current_date = datetime.datetime.utcnow()
            start_of_day = datetime.datetime(current_date.year, current_date.month, current_date.day)
            start_of_day_month_ago = start_of_day - datetime.timedelta(days=30)


            if user_version:
                req_qeury = queries.get_request(session, "version", ktru_number, start_of_day_month_ago, user_version)
            else:
                req_qeury = queries.get_request(session, "version", ktru_number, start_of_day_month_ago)

            if req_qeury:
                if req_qeury.isSuccess:
                    msg[3] = "version - DB"
                    print_stage(msg, print_stage_on)

                    if user_version:
                        db_latest_version = queries.get_user_version_for_ktru(session, ktru, user_version)
                    else:
                        db_latest_version = queries.get_latest_version_for_ktru(session, ktru)
                    parsed_version_number = db_latest_version.versionNumber
                else:
                    db_failed_request_exist = True
                    need_new_parse = True
            else:
                need_new_parse = True

            if need_new_parse:
                msg[3] = "version - parsing..."
                print_stage(msg, print_stage_on)
                if user_version:
                    # нет парсера для версии (не нужен, надеюсь)
                    version_info = {"version": user_version, "date": "27.05.1703"}
                else:
                    html = fetch_for_parse_version(session, ktru_number)

                    version_info = parse_ktru_version(html)

                # Ожидается, что parse_ktru_version возвращает словарь вида {"version": int, "date": str}
                parsed_version_number = version_info.get("version")

                if parsed_version_number is None:
                    raise BusinessError("Parsed version number is missing")

                date_str = version_info.get("date")  # ожид: '04.08.2025'
                parsed_version_date = None
                try:
                    # убедиться, что это строка
                    if date_str:
                        parsed_version_date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
                except ValueError:
                    logger.exception("Failed to strptime parsed_version_date %s", date_str)
                except Exception:
                    logger.exception("Unexpected error while parsing date %s", date_str)
                if db_failed_request_exist:
                    # меняем лог на успешный парсинг
                    req_qeury.isSuccess = True
                    session.add(req_qeury)
                else:
                    queries.log_request(session, "version", True, ktru_number, parsed_version_number)
                msg[3] = "version - Parsed"
                print_stage(msg, print_stage_on)

            # 3. Получаем последнюю версию в БД (если есть)
            msg[4] = "chars - checking DB..."
            print_stage(msg, print_stage_on)

            if user_version:
                db_latest_version = queries.get_user_version_for_ktru(session, ktru, user_version)
            else:
                db_latest_version = queries.get_latest_version_for_ktru(session, ktru)

            db_latest_number = db_latest_version.versionNumber if db_latest_version else None

            if db_latest_number == parsed_version_number:
                # версии совпали - пытаемся получить характеристики из БД
                chars = queries.get_chars_for_version(session, db_latest_version)
                msg[4] = "chars - DB"
                if not chars:
                    msg[4] = "chars - DB-None, parsing..."
                    print_stage(msg, print_stage_on)
                    # если в БД нет характеристик — парсим их из HTML
                    html = fetch_for_pasrse_chars(session, ktru_number, db_latest_number)
                    parsed_chars = parse_ktru_chars_table_from_html(html)
                    # parsed_chars ожидается как список dict с ключами: name, values, unit
                    if parsed_chars:
                        queries.create_ktru_chars_bulk(session, db_latest_version, parsed_chars)
                        chars = queries.get_chars_for_version(session, db_latest_version)
                        logger.info("Parsed and stored chars for existing version %s of ktru %s", parsed_version_number, number)

                    msg[4] = "chars - Parsed"
                char_num = len(chars) if chars else 0
                msg[4] = msg[4] + "(" + str(char_num) + ")"
                print_stage(msg, print_stage_on)
                msg[5] = ktru.name + ' (' + str(parsed_version_number) + ')'
                print_stage(msg, print_stage_on)
                result = {
                    "ktru_id": ktru.id,
                    "name": ktru.name,
                    "number": ktru.number,
                    "unit": ktru.unit,
                    "ownCharsIsForbidden": ktru.ownCharsIsForbidden,
                    "version": parsed_version_number,
                    "chars_count": char_num,
                    "chars": ktru_chars_to_dicts(chars)
                }
            else:
                msg[4] = "chars - DB-None, parsing..."
                print_stage(msg, print_stage_on)
                # версии разные или в БД нет версии — создаём новую версию и парсим характеристики
                new_version = queries.create_ktru_version(session, ktru.id, parsed_version_number, parsed_version_date)
                html = fetch_for_pasrse_chars(session, ktru_number, new_version.versionNumber)
                parsed_chars = parse_ktru_chars_table_from_html(html)
                if parsed_chars:
                    queries.create_ktru_chars_bulk(session, new_version, parsed_chars)
                    chars = queries.get_chars_for_version(session, new_version)
                    msg[4] = "chars - Parsed"
                else:
                    chars = []
                char_num = len(chars) if chars else 0
                msg[4] = msg[4] + "(" + str(char_num) + ")"
                print_stage(msg, print_stage_on)
                msg[5] = ktru.name + ' (' + str(parsed_version_number) + ')'
                print_stage(msg, print_stage_on)
                result = {
                    "ktru_id": ktru.id,
                    "name": ktru.name,
                    "number": ktru.number,
                    "unit": ktru.unit,
                    "ownCharsIsForbidden": ktru.ownCharsIsForbidden,
                    "version": parsed_version_number,
                    "chars_count": len(chars),
                    "chars": ktru_chars_to_dicts(chars)
                }

            return result

    except SQLAlchemyError:
        logger.exception("Database error during processing of Ktru %s", number)
        raise BusinessError("Database error")
    except Exception:
        logger.exception("Unexpected error during processing")

        raise
