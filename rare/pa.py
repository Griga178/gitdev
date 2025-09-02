'''
    Зона теста

    - парсер ozon
    открыть браузер с '--remote-debugging-port=9222'
    подключиться к порту 9222
    управлять через websocket

'''
from websocket import create_connection
import subprocess
import os
import requests
import json
from contextlib import contextmanager

from bs4 import BeautifulSoup


# Путь к yandex browser (обычное расположение в Windows)
path = r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'
yandex_path = os.path.expandvars(path)

# Запуск браузера

url1 = 'https://www.ozon.ru/product/komplekt-trusov-boksery-vienece-trusy-muzhskie-4-sht-1615748876/?at=XQtkPlmAQhDn38JKcXmOlArCxrJ8znsvxWVEgFVok1vV'
url2 = 'https://nc.lordfilm12.ru/'
br_set = {
    'max': '--start-maximized',        # окно максимизировано
    'full': '--start-fullscreen',      # полноэкранный режим
    'kiosk': '--kiosk',               # режим киоска (полный экран без управления)
    'incognito': '--incognito',       # режим инкогнито
    'headless': '--headless',         # безголовый режим (без GUI)
    'app': '--app=URL',                # режим приложения с одной вкладкой
    'window_size': '--window-size=width,height',   # размер окна
    'window_pos': '--window-position=x,y',         # позиция окна

    'allow_origins': '--remote-allow-origins=http://localhost:9222',
    'port': '--remote-debugging-port=9222'
}

subprocess.Popen([yandex_path, url1, br_set['max'], br_set['port'], br_set['allow_origins']])

# Получаем список открытых табов (целевых страниц)
response = requests.get('http://localhost:9222/json')
tabs = response.json()
# print(tabs)

# Выбираем первый таб
tab = tabs[0]
print(tab)

# URL для подключения к WebSocket
websocket_url = tab['webSocketDebuggerUrl']

# Контекстный менеджер для WebSocket соединения
@contextmanager
def websocket_connection(ws_url):
    ws = create_connection(ws_url)
    try:
        yield ws
    finally:
        ws.close()

# Функция для отправки команд в DevTools Protocol
def send_command(ws, method, params=None, id=1):
    message = {
        'id': id,
        'method': method
    }
    if params:
        message['params'] = params
    ws.send(json.dumps(message))
    return id + 1

# Используем with для подключения к WebSocket и получения кода страницы
with websocket_connection(websocket_url) as ws:
    id = 1
    # Включаем Runtime
    id = send_command(ws, 'Runtime.enable', id=id)
    ws.recv()  # Принимаем ответ без обработки, чтобы не мешать порядку

    # Запрашиваем HTML документ через document.documentElement.outerHTML
    expression = 'document.documentElement.outerHTML'
    id = send_command(ws, 'Runtime.evaluate', {'expression': expression, 'returnByValue': True}, id)

    # Получаем ответ и парсим содержимое страницы
    while True:
        result = ws.recv()
        response_data = json.loads(result)
        if 'id' in response_data and response_data['id'] == id - 1:
            html_content = response_data.get('result', {}).get('result', {}).get('value')
            break

print('Код страницы для парсинга получен:')
# print(html_content)

soup = BeautifulSoup(html_content, 'html.parser')
# Находим первый блок с data-widget="webSale"
# web_sale_block = soup.find('div', attrs={'data-widget': 'webSale'})

# Внутри него ищем блок с data-widget="webPrice"
# web_price_block = web_sale_block.find('div', attrs={'data-widget': 'webPrice'})
web_price_block = soup.find('div', attrs={'data-widget': 'webPrice'})

print(web_price_block)

# закрытие отпарсеной страницы
with websocket_connection(websocket_url) as ws:
    target_id =tabs[0]['id']
    close_cmd = {
        "id": 1, # нужно менять
        "method": "Target.closeTarget",
        "params": {"targetId": target_id}
    }
    ws.send(json.dumps(close_cmd))
    result = ws.recv()
    print(result)
'''
<div class="m9p_28" data-widget="webPrice" params="[object Object]">
    <!-- -->
    <div class="m8p_28">
        <div class="p4m_28 a201-a a201-a3">
            <button class="a201-a4 a201-a3" style="border-radius:8px;" tabindex="0" type="button">
                <span class="a201-b1 a201-d6 a201-f0 a201-a3" style="border-radius:8px;">
                    <div class="n7k_28">
                        <div class="kn8_28 nk8_28">
                            <div class="mp5_28">
                                <div class="m5p_28 pm4_28">
                                    <span class="p7m_28 mp6_28">503 ₽</span>
                                <!-- -->
                                </div>
                            <span class="p5m_28 pm4_28">c Ozon Картой</span>
                            </div>
                        </div>
                        <div class="kn9_28 k9n_28">
                            <svg class="nk9_28" height="16" width="16" xmlns="http://www.w3.org/2000/svg">
                                <path d="M5.293 12.293a1 1 0 1 0 1.414 1.414l5-5a1 1 0 0 0 0-1.414l-5-5a1 1 0 0 0-1.414 1.414L9.586 8z" fill="currentColor">
                                </path>
                            </svg>
                        </div>
                    </div>
                </span>
            </button>
        </div>
        <!-- -->
        <div class="q0m_28 q5m_28">
            <div class="q3m_28">
                <div class="mq4_28">
                    <span class="mq2_28 m2q_28 mq6_28">530 ₽</span>
                    <!-- -->
                    <span class="qm1_28 qm2_28 qm0_28 q1m_28">2 999 ₽</span>
                    <!-- -->
                </div>
                <div class="m3q_28">
                    <span class="qm1_28 q1m_28">без Ozon Карты</span>
                </div>
            </div>
            <!-- -->
        </div>
        <!-- -->
    </div>
    <!-- --> <!-- -->
    <div><!-- --></div>
    <!-- -->
</div>
'''
