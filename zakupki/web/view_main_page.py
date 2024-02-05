from flask import render_template, url_for, request
from .models import *


from .module_parser import Parse_app

def launch_product_pars():
    pass

def launch_contract_checking():
    pass


mini_app = Parse_app(app, Contrant_card)


@app.route('/refresh_app', methods = ('GET', 'POST'))
def refresh_app():
    mini_app.refresh_app()
    return 'True'

@app.route('/check_counter', methods = ('GET', 'POST'))
def check_counter():
    return mini_app.get_info()

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html', **mini_app.get_info())

@app.route('/parse_numbers', methods = ('GET', 'POST'))
def parse_numbers():

    # Сообщение об настройке дат от проги True/ Error {Message}
    message_about_dates = mini_app.set_dates(**request.form)
    if message_about_dates != True:
        return message_about_dates
    mini_app.parse_numbers()
    return mini_app.get_info()

@app.route('/stop_app', methods = ('GET', 'POST'))
def stop_app():
    mini_app.is_active = 0
    return 'True'

def check_old_dates():
    '''
        Проверяет наличие новых-исполненных контрактов
        за выбранный период, после первичного парсинга
        - при наличии - скачивает

    '''
    pass
