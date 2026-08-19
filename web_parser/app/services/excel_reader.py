# app/services/excel_reader.py

from typing import List, Union
from pathlib import Path, WindowsPath
import openpyxl
import logging
import re

def get_domain(link:str) -> str:
    pass

def validate_link(link:str) -> Union[str, None]:
    if link[:4] == 'http':
        return link
    else:
        return None

def get_domain(link:str) -> str:
    split_list = link.split("/")
    return split_list[2]

def read_link(link_cell:str, logger, row_counter) -> Union[str, None]:
    '''
        если в строке больше 1 ссылки   -> None
        если строка пустая              -> None
        если ссылка не валидна          -> None
        иначе                           -> (domain, link)
    '''
    if link_cell:
        parts = re.findall(r'[\w:,()|/.\-?=&+%#\[\]]+', link_cell)
        if len(parts) > 1:
            logger.info(f"Больше 1 ссылки, строка {row_counter+1}")
            return None

        link = validate_link(parts[0])
        if link:
            
            return (get_domain(link), link)
        else:
            logger.info(f"Ссылка не валидна строка: {row_counter+1}, {link}")
            return None

    else:
        # пустая ячейка - это нормально
        return None

def extract_links_from_excel(file_source: Union[str, Path], column:int=None) -> List[str]:
    '''
        функция принимает стандартную рабочую таблицу, где ссылки
        находятся в столбце "S"| № 19 | [18] | "Ссылка",
        на первом листе[0]
        сделан 1 вариант под индекс столбца и первый лист
    '''
    print('hello', type(file_source)==WindowsPath)
    logger = setup_logger("extract_links_from_excel", "extract_links_from_excel.log")
    logger.info("=== Открываем excel файл ===")

    if type(file_source) == str:
        file_path = Path(file_source)
    elif type(file_source) == WindowsPath:
        file_path = file_source
    else:
        print('неизвестный тип файла')
        logger.info(f"неизвестный тип файла: {type(file_source)} ({file_source})")

    links_clm_num = 18
    work_book = openpyxl.load_workbook(file_source, read_only = True, data_only = True)
    active_sheet = work_book.worksheets[0]
    rows_generator = active_sheet.iter_rows(min_row = 2)

    links = []
    row_counter = 0
    l_counter = 0
    # читаем строки
    for row in rows_generator:
        row_counter += 1
        raw_links = read_link(row[links_clm_num].value, logger, row_counter)


    # разложение строк на link, domain не валидное отбрасываем

    # возврат
