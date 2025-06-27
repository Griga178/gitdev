import os
import subprocess
import json
import requests
from websocket import create_connection
from contextlib import contextmanager
import time

class MyBrowser():
    def __init__(self, path=None):
        self.path = path if path else r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'
        self.yandex_path = os.path.expandvars(self.path)
        self._is_launch = False
        self.ws = None  # текущее websocket соединение
        self.last_id = 0

    def launch(self, *param_list):
        ''' запуск браузера '''
        print('launch')
        # Добавляем параметры для remote debugging
        param_list = list(param_list)
        param_list.append('--remote-debugging-port=9222')
        param_list.append('--remote-allow-origins=http://localhost:9222')
        param_list.append('--start-maximized')
        subprocess.Popen([self.yandex_path, *param_list])
        # Ждем пока браузер запустится и откроется порт
        time.sleep(2)
        # Запрашиваем список вкладок
        response = requests.get('http://localhost:9222/json')
        self.tabs = response.json()
        self._is_launch = True
        print('launch end')

    @contextmanager
    def websocket_connection(self, tab=None):
        ''' Контекстный менеджер подключения к WebSocket одной из вкладок '''
        if tab is None:
            # по умолчанию берем первую вкладку (если есть)
            tab = self.tabs[0]
        ws_url = tab['webSocketDebuggerUrl']
        self.ws = create_connection(ws_url)
        try:
            yield self.ws
        finally:
            self.ws.close()
            self.ws = None

    def _send_command(self, method, params=None, timeout=5):
        self.last_id += 1
        message = {
            'id': self.last_id,
            'method': method,
            'params': params or {}
        }
        self.ws.send(json.dumps(message))

        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for response to {method}")

            try:
                response = json.loads(self.ws.recv())
            except Exception as e:
                continue

            # Фильтруем ответ по id
            if 'id' in response and response['id'] == self.last_id:
                return response

    def get_url(self, url):
        print('get_url')
        if not self._is_launch:
            self.launch()
            time.sleep(2)
            # Обновим вкладки после запуска
            response = requests.get('http://localhost:9222/json')
            self.tabs = response.json()

        # Подключаемся к первой вкладке через websocket
        with self.websocket_connection(self.tabs[0]) as ws:
            print('websocket_connection - open')
            self.ws = ws

            # Навигируем к нужному URL
            self._send_command('Page.navigate', {'url': url})

            # Ждём загрузку страницы (ждем событие Page.loadEventFired)
            print('Ждём загрузку')
            while True:
                resp = json.loads(self.ws.recv())
                if resp.get('method') == 'Page.loadEventFired':
                    break

            # Включаем Runtime
            print('Включаем Runtime')
            self._send_command('Runtime.enable')
            print('Включаем Runtime - ok')
            # Запрашиваем HTML страницы
            print('Запрашиваем HTML страницы')
            res = self._send_command('Runtime.evaluate', {
                'expression': 'document.documentElement.outerHTML',
                'returnByValue': True
            })
            print('Запрашиваем HTML страницы - ok')
            url_content = res['result']['result']['value']
            return url_content

    def close_url(self, target_id):
        # Закрываем вкладку по targetId через HTTP API
        requests.get(f'http://localhost:9222/json/close/{target_id}')
        # Обновляе� список вкладок
        response = requests.get('http://localhost:9222/json')
        self.tabs = response.json()

    def get_content(self, url_id):
        # Получаем контент по url_id (targetId вкладки)
        tab = next((t for t in self.tabs if t['id'] == url_id), None)
        if not tab:
            return None

        with self.websocket_connection(tab) as ws:
            self.ws = ws
            # Включаем Runtime
            self._send_command('Runtime.enable')

            # Получаем title
            title_res = self._send_command('Runtime.evaluate', {
                'expression': 'document.title',
                'returnByValue': True
            })

            # Получаем HTML
            html_res = self._send_command('Runtime.evaluate', {
                'expression': 'document.documentElement.outerHTML',
                'returnByValue': True
            })

            return {
                'title': title_res['result']['result']['value'],
                'html_content': html_res['result']['result']['value']
            }

    def quit(self):
        # Закрываем все вкладки и отключаемся
        if self._is_launch:
            for tab in self.tabs:
                try:
                    self.close_url(tab['id'])
                except Exception:
                    pass
            self._is_launch = False


browser = MyBrowser()
url = 'https://www.ozon.ru/product/komplekt-trusov-boksery-vienece-trusy-muzhskie-4-sht-1615748876/'
html = browser.get_url(url)
print(html)

# Получить список вкладок
print(browser.tabs)

# Получить контент по id вкладки
content = browser.get_content(browser.tabs[0]['id'])
print(content['title'])

# Закрыть вкладку
browser.close_url(browser.tabs[0]['id'])

# Закрыть браузер (закрыть все вкладки)
browser.quit()
