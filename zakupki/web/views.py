from flask import render_template, url_for, request
from flask_table import Table, Col, DateCol, LinkCol
# https://flask-table.readthedocs.io/en/stable/#table-configuration-and-options
from .models import *


@app.route('/')
@app.route('/contracts')
def contracts():
    # contracts = Contrant_card.query
    # , title = 'Table'
    return render_template('main.html')#, contracts = contracts)

@app.route('/api/contracts')
def data():
    return {'data': [contract.to_dict() for contract in Contrant_card.query]}

@app.route('/api/products')
def api_products():
    return {'data': [product.to_dict() for product in Product.query]}


@app.route('/products', methods = ('GET', 'POST'))
def products():

    return render_template('products.html', title = 'Товары')

@app.route('/products_v2')
def products_v2():

    return render_template('products_v2.html', title = 'Товары 2.0')

def reform_im_dict(imm_dict):
    data = {'columns': [], 'order': []}

    for el in imm_dict:
        if 'columns' in el:
            keys = el.split('[')
            keys = [i.replace(']','') for i in keys]
            data['columns'][keys[1]]

        if ']' in el:
            keys = el.split('[')
            keys = [i.replace(']','') for i in keys]
            print(keys)
        else:
            print(el)


@app.route('/api/products_v2', methods = ('GET', 'POST'))
def api_products_v2():

    draw = request.form['draw'] # "счетчик" +1 при новом запросе
    row = int(request.form['start']) # номер начальной строки
    rowperpage = int(request.form['length']) # количество выводимых строк
    searchValue = request.form["search[value]"] # строка для поиска
    # print(request.form['columns[1][search][value]'])

    # for el in request.form:
    #     print(f'{el}: {request.form[el]}')
        # print([el])
    reform_im_dict(request.form)
    pq = Product.query.offset(row).limit(rowperpage)
    if searchValue != '':
        pass
        # pq.like

        # print(request.form.columns)

    print(searchValue)
    return {'data': [product.to_dict() for product in pq]}
