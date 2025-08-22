
# project/controller/controller.py
"""
Controller
Высокоуровневая логика приложения: координация работы парсера, сервисов и БД.
Содержит заглушки методов — имена и сигнатуры для быстрой навигации по проекту.
"""
from zakupki.services.business import fetch_parse_and_store_ktru

from typing import Any, List, Optional

class Controller:
    fetch_parse_and_store_ktru = fetch_parse_and_store_ktru
    def __init__(self):

        self.fetch_parse_and_store_ktru = Controller.fetch_parse_and_store_ktru
