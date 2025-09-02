# RemBrowseControl

## Описание
Утилита для управления браузером с запущенным удалённым отладчиком на http://localhost:9222/,  
позволяющая выполнять парсинг под видом обычного пользователя.

---

## Возможности

- Запуск браузера с режимом удалённого отладчика  
- Открытие новой вкладки с заданным URL и получение её ID  
- Получение HTML содержимого вкладки по ID  
- Закрытие вкладки по ID  
- Закрытие браузера  

---

## Пример использования

```python
from rbc.controller import RemBrowseControl

rbc = RemBrowseControl()
rbc.run()                  # Запуск браузера

id = rbc.new_tab(url)      # Открытие вкладки, возвращается ID  
html_content = rbc.get_content(id)  # Получение HTML содержимого вкладки  

data = parse_func(html_content) # парсинг HTML

rbc.close_tab(id)          # Закрытие вкладки  
rbc.close()                # Закрытие браузера
