# scripts/import_links_cli.py
"""
Скрипт для импорта ссылок из Excel через командную строку.

1 формирование списка ссылок
2 формирование domain, link, file_path, date
3 сохранение в БД

Пример запуска:
указание пути во время запуска
import_links_cli.py --file /path/to/file.xlsx

указание пути после запуска
import_links_cli.py

import_links_cli.py --file "C:/Users/G.Tishchenko/Desktop/4 кв 2026/26. Оборудование.xlsx"
"""
import argparse
import sys
import logging
from pathlib import Path

# Добавляем корень проекта в sys.path, чтобы импортировать модули app
sys.path.append(str(Path(__file__).parent.parent))
from app.services.excel_reader import extract_links_from_excel
from app.utils.logger import setup_logger   # импортируем наш логгер

def main():
     # Настраиваем логгер специально для этого скрипта
    logger = setup_logger("import_cli", "import.log")
    logger.info("=== ЗАПУСК СКРИПТА ИМПОРТА ===")

    parser = argparse.ArgumentParser(description='Импорт ссылок из Excel')
    parser.add_argument('--file', '-f', help='Путь к Excel-файлу')
    # Можно изменить индекс колонки
    parser.add_argument('--column', '-c', default=0, type=int, help='Номер колонки (по умолчанию 0)')

    args = parser.parse_args()

    if args.file is None:
        input_row = input("Введите путь до файла: ").strip()
        if not input_row:
            print('пусто -> выход')
            sys.exit(1)
        file_path = Path(input_row)
        logger.info(f"Путь введён пользователем: {file_path}")
    else:
        file_path = Path(args.file)
        logger.info(f"Путь передан через аргумент: {file_path}")

    if not file_path.exists():
        logger.error(f"Файл не найден: {file_path}")
        sys.exit(1)

    logger.info(f"Файл существует")
    try:
        logger.info("Начинаем извлечение ссылок из Excel...")
        links = extract_links_from_excel(file_path)
        logger.info(f"Успешно получено {len(links)} ссылок:")

        # Здесь вы можете добавить логику сохранения в БД, если нужно
        for link in links:
            print(link)  # или сохранить в БД
        # логика для БД
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
