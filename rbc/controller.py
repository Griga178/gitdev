import sys
import subprocess
import os
import requests
import json
from websocket import create_connection
from contextlib import contextmanager

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

class RemBrowseControl():
    """
        Запуск браузера с режимом отладчика

        kw ключи:
            browser: str ["yandex", edge]
            remote_port : int - порт для подключения к браузеру

        self.path: str - путь до C:/<бразера>.exe
        self.br_subprocess_name: str - имя процесса для - проверки/завершения работы
        self.browser_running: bool - Флаг, указывающий, запущен ли браузер (True — запущен, False — нет).
        self.remote_port: int -порт для подключения к браузеру

        self.tabs - словарь открытых вкладок по ключу id.
        Каждая вкладка — словарь с ключами:
        - description — строка, описание вкладки (часто пустая).
        - devtoolsFrontendUrl — URL для доступа к DevTools интерфейсу этой вкладки через браузер.
        - id — уникальный идентификатор вкладки.
        - processId — идентификатор системного процесса, связанного с вкладкой.
        - title — заголовок вкладки (обычно название страницы).
        - type — тип вкладки (например, "page", "other" и т.п.).
        - url — URL открытой страницы в вкладке.
        - webSocketDebuggerUrl — WebSocket URL для взаимодействия с вкладкой через протокол отладки Chrome.

    """

    def __init__(self, **kw):
        self.path = r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'
        self.br_subprocess_name = 'browser.exe'

        if kw.get('browser', None):
            if kw['browser'].lower() == 'edge':
                self.path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
                self.br_subprocess_name = 'msedge.exe'
            elif kw['browser'].lower() == 'yandex':
                # по дефолту яндекс
                pass

        # проверки
        if not os.path.isfile(self.path):
            print(f"Ошибка: файл '{self.path}' не найден.")
            sys.exit(1)  # Останавливаем выполнение скрипта

        self.remote_port = kw.get('remote_port', 9222)
        self.user_name = os.getlogin()  # Получаем имя текущего пользователя

        # закрываем браузер если уже открыт без режима удаленного управления
        self.browser_running = self.check_and_close_browser()

        self.tabs = {}

    def check_and_close_browser(self):
        try:
            response = requests.get(f'http://localhost:{self.remote_port}/json')
            # Если запрос прошёл успешно (код 200)
            if response.status_code == 200:
                print('браузер открыт в нужном режиме')
                return True
            else:
                raise Exception("Ответ сервера не 200")
                return False
        except Exception:
            # Если ошибка при запросе, проверяем, запущен ли браузер
            self.close()

    def run(self):

        # настройки для запуска браузера в особом режиме
        if self.br_subprocess_name == 'browser.exe':
            user_data_str = f'--user-data-dir=C:/Users/{self.user_name}/AppData/Local/Yandex/YandexBrowser/User Data'
        elif self.br_subprocess_name == 'msedge.exe':
            user_data_str = f'--user-data-dir=C:/Users/{self.user_name}/AppData/Local/Microsoft/Edge/User Data'
        settings = [
            self.path,
            # '--window-position=0,0',
            # '--window-size=1920,1080',
            '--start-maximized',
            f'--remote-debugging-port={self.remote_port}',
            f'--remote-allow-origins=http://localhost:{self.remote_port}',
            user_data_str,
            '--profile-directory=Default'
        ]

        if not self.browser_running:
            subprocess.Popen(settings)

        tabs = requests.get(f'http://localhost:{self.remote_port}/json').json()
        self.tabs = {tab['id']: tab for tab in tabs}

    def new_tab(self, url:str) -> str:
        """ возвращает id вкладки в self.tabs """

        try:
            # Создаём новую вкладку с нужным URL
            # инфа без title и url юзера
            new_tab = requests.put(f'http://localhost:{self.remote_port}/json/new?{url}').json()

            new_tab_id = new_tab['id']
            self.tabs[new_tab_id] = new_tab
            # print(new_tab)
            # ws_url = new_tab['webSocketDebuggerUrl']
            # # тут текущий url
            # mytabs = requests.get(f'http://localhost:{self.remote_port}/json').json()
            # tab_info = next((tab for tab in mytabs if tab['id'] == new_tab_id), None)
            # print(tab_info)

            return new_tab_id

        except Exception as e:
            print('Ошибка при открытии вкладки:', e)

        return None

    def close_tab(self, tab_id: str) -> None:
        try:
            response = requests.get(f'http://localhost:{self.remote_port}/json/close/{tab_id}')
            if response.ok:
                del self.tabs[tab_id]
            else:
                print('Не удалось закрыть вкладку:', response.text)
        except Exception as e:
            print('Ошибка при закрытии вкладки:', e)

    def get_content(self, tab_id: str) -> str:
        ws_url = self.tabs[tab_id]['webSocketDebuggerUrl']
        with websocket_connection(ws_url) as ws:
            id = 1
            # Включаем Runtime
            id = send_command(ws, 'Runtime.enable', id=id)
            message = ws.recv()  # Принимаем ответ без обработки, чтобы не мешать порядку
            # print(message)
            # Запрашиваем HTML документ через document.documentElement.outerHTML
            expression = 'document.documentElement.outerHTML'
            id = send_command(ws, 'Runtime.evaluate', {'expression': expression, 'returnByValue': True}, id)

            # Получаем ответ и парсим содержимое страницы
            while True:
                result = ws.recv()
                response_data = json.loads(result)
                if 'id' in response_data and response_data['id'] == id - 1:
                    html_content = response_data.get('result', {}).get('result', {}).get('value')
                    return html_content
                    break

    def close(self):
        try:
            output = subprocess.check_output('tasklist', shell=True, text=True).lower()
            if self.br_subprocess_name in output:
                # Закрываем браузер
                subprocess.run(f'taskkill /f /im {self.br_subprocess_name}', shell=True, check=True)
                # return "Браузер был открыт, теперь закрыт"
                return False
            else:
                # return "Ошибка: браузер не запущен"
                return False
        except subprocess.CalledProcessError:
            raise Exception("Ошибка при работе с процессами")
            return False
