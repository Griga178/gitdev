from flask import render_template, url_for, request
from .models import *

from .parse_v2 import Parser_ver_2


parse_app = Parser_ver_2(
    app = app,
    db = db,
    Contrant_card = Contrant_card,
    Product = Product
    )


@app.route('/refresh_app', methods = ('GET', 'POST'))
def refresh_app():

    parse_app.refresh_app()
    return 'True'

@app.route('/check_counter', methods = ('GET', 'POST'))
def check_counter():

    return parse_app.get_info()

@app.route('/')
@app.route('/main')
def main():

    return render_template('main.html', **parse_app.get_info())

@app.route('/parse_numbers', methods = ('GET', 'POST'))
def parse_numbers():
    ''' запуск парсера '''

    parse_app.set_dates(**request.form)
    parse_app.parse_contract_numbers()
    return parse_app.get_info()


@app.route('/stop_app', methods = ('GET', 'POST'))
def stop_app():
    parse_app.is_active = 0
    return 'True'

def check_old_dates():
    '''
        Проверяет наличие новых-исполненных контрактов
        за выбранный период, после первичного парсинга
        - при наличии - скачивает

    '''
    pass
