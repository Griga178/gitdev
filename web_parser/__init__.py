```markdown
# Парсер (parser)

В этой папке находится класс/функции для парсинга HTML с помощью библиотеки BeautifulSoup.

### Описание

- Парсер принимает на вход:

  - настройки для каждого сайта в виде словаря (в дальнейшем из БД)
  - HTML-контент страницы

- На выходе возвращает данные, указанные в настройках (позже сохраняются в БД)
- Используется логирование для удобства отладки и мониторинга

### Структура

├── parser/
│   ├── __init__.py
│   ├── parser.py       — класс/функции для парсинга с bs4
│   ├── logger.py       — настройка логирования
│   ├── models.py       — таблицы БД
│   ├── utils.py        — вспомогательные функции (по необходимости)
```

```python
import requests
from web_parser import parse

url = 'https://github.com/123'
domain = "github.com" # из url
settings = {"github.com": {"price":"div;class;price", "name":"div;class;name"}}

html_content = requests.get(url)
data = parse(html_content, settings[domain])

```

## Таблицы
```python
...
# Проект
class WebPage(Base):
    __tablename__ = 'webPage'
    id = Column(Integer, primary_key=True)
    name = Column(Text) # домен сайта "github.com"

    settings = relationship("Settings", back_populates="webPage")
    parsed_data = relationship("ParsedData", back_populates="webPage")


class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    body = Column(Text) # настройки в формате json

    web_page_id = Column(Integer, ForeignKey('webPage.id'), nullable=False)


class ParsedData(Base):
    __tablename__ = 'parsedData'
    id = Column(Integer, primary_key=True)
    url = Column(Text) # ссылка
    date = Column(DateTime)
    screen_id = Column(Text) # id скриншота
    body = Column(Text) # результат парсинга в формате json

    web_page_id = Column(Integer, ForeignKey('webPage.id'), nullable=False)
```
