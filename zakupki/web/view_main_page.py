from flask import render_template, url_for, request
from .models import *


from .module_parser import Parse_app

def launch_contract_number_pars():

    pass

def launch_product_pars():
    pass

def launch_contract_checking():
    pass

def get_view():
    '''
        Сводка данных из таблицы
        Кол-во контрактов
            по годам
            отпарсено

        кол-во товаров

        кол-во компаний

        кол-во ККН

    '''

    pass


mini_app = Parse_app()

@app.route('/run_app', methods = ('GET', 'POST'))
def run_app():
    mini_app.run_app()
    return str(mini_app.start_counter)

@app.route('/stop_app', methods = ('GET', 'POST'))
def stop_app():
    mini_app.stop_app()
    return str(mini_app.stop_counter)

@app.route('/check_counter', methods = ('GET', 'POST'))
def check_counter():
    return str(mini_app.counter)

@app.route('/')
@app.route('/main')
def main():
    last_contract_date = '2023-11-30'
    end_contract_date = '2024-01-11'
    return render_template('main.html',
    ecd = end_contract_date,
    lcd = last_contract_date,
    start_times = mini_app.start_counter,
    stop_times = mini_app.stop_counter,
    main_times = mini_app.counter)

@app.route('/parse_numbers', methods = ('GET', 'POST'))
def parse_numbers():
    forms_req = request.form
    print(forms_req)


    return 'Parser launched'


def check_old_dates():
    '''
        Проверяет наличие новых-исполненных контрактов
        за выбранный период, после первичного парсинга
        - при наличии - скачивает

    '''
    pass

def check_old_contracts():
    '''
    фильтр номеров по дате обновления
    '''
    pass
