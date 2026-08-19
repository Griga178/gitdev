# app/utils/logger.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "app", log_file: str = "app.log") -> logging.Logger:
    """
    Настраивает и возвращает логгер с ротацией файлов.
    """
    # Создаём директорию для логов, если её нет

    BASE_DIR = Path(__file__).parent.parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)   # создаём папку, если её нет

    log_path = LOG_DIR / log_file

    # Создаём логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)   # Уровень для всего логгера

    # Формат: время - уровень - имя модуля - сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для файла (с ротацией)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10_000_000,  # 10 МБ
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)  # В файл пишем только INFO и выше
    file_handler.setFormatter(formatter)

    # Обработчик для консоли (удобно при разработке)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # В консоль можно выводить всё
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
