# Парсер (parser)

В этой папке находится класс/функции для парсинга HTML с помощью библиотеки BeautifulSoup.

### Описание

- Парсер принимает на вход:

  - настройки для каждого сайта в виде словаря (в дальнейшем из БД)
  - HTML-контент страницы

- На выходе возвращает данные, указанные в настройках (позже сохраняются в БД)
- Используется логирование для удобства отладки и мониторинга

### Структура

├── web_parser/
│   ├── __init__.py
│   ├── parser.py       — класс/функции для парсинга с bs4
│   ├── logger.py       — настройка логирования
│   ├── models.py       — таблицы БД
│   ├── utils.py        — вспомогательные функции (по необходимости)

## models.py

`SiteInfo`
    name - домен сайта "github.com"
    settings - настройки в формате json

`ParseResult`
    url - ссылка
    date - дата парсинга
    screenshot - имя скриншота (совпадает с названием файла {path}{screen_id}.jpg)
    data - результат парсинга в формате json
    site_info_id - FK

+ Структура SiteInfo.settings
  `url`         - str, optional
  `domain`      - str, req
  `date`        - datetime.now, func
  `screenshot`  - str, optional если нет, формируем сами (id сайта + datetime.ms)
  `search_data` - list[search_data_dict]
---
+ Структура search_data_dict - путь/алгоритм и проч для поиска данных, ключи:
  `name`        - str - название искомого (price/name/old_price, ...)
  `type`        - str - ожидаемый тип данных (str, float, bool)
  `rules`       - list[rule_dict] - списко правил поиска, позволяет адаптироваться под разные структуры
---
+ Структура rule_dict
  `search_index`   - 0, - если больше 0 находит все такие теги и выбирает по индексу
  `tag_name`      - "div",
  `attr_name`     - "class",
  `attr_value`    - "price",
  `target_point`  - True, либо еще один вложенный rule_dict

rule_dict
## Пример использования

```python
import requests
from web_parser import parse_html

url = 'https://github.com/123'
domain = "github.com" # из url
settings = {"github.com": {"price":"div;class;price", "name":"div;class;name"}}

html_content = requests.get(url)
data = parse_html(html_content, settings[domain])
