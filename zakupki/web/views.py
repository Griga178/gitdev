from flask import Flask, url_for, request
from flask import render_template

app = Flask(__name__, template_folder = "templates")

app.config['SECRET_KEY'] = 'AASDFASDF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/zakupki2.db'

app.debug =  True


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Contrant_card(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    customer = db.Column(db.Text)
    update_date = db.Column(db.DateTime)

    provider_id = db.Column(db.ForeignKey('company.inn'))

    products = db.relationship("Product", backref = 'contract')

    def to_dict(self):
        return {
            'number': str(self.number),
            'date': self.date.strftime('%d.%m.%Y'),
            'price': self.price,
            'update_date': self.update_date.strftime('%d.%m.%Y') if self.update_date else None,
        }

class Company(db.Model):
    inn = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    phone = db.Column(db.Text)
    e_mail = db.Column(db.Text)

    addres = db.Column(db.Text)

    contrants = db.relationship("Contrant_card", backref = 'contract')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    country_producer = db.Column(db.Text)
    ktru = db.Column(db.Text)
    okpd_2 = db.Column(db.Text)
    type = db.Column(db.Text)
    measure = db.Column(db.Text)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    cost = db.Column(db.Float)
    tax = db.Column(db.Text)

    contrant_card_id = db.Column(db.ForeignKey("contrant_card.number"))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_producer': self.country_producer,
            'ktru': self.ktru,
            'okpd_2': self.okpd_2,
            'type': self.type,
            'quantity': self.quantity,
            'measure': self.measure,
            'price': self.price,
            'cost': self.cost,
            'tax': self.tax,
            'contrant_card_id': str(self.contrant_card_id),
            'contrant_card_date': self.contract.date.strftime('%d.%m.%Y'),
        }

with app.app_context():
    db.create_all()

from flask_table import Table, Col, DateCol, LinkCol
# https://flask-table.readthedocs.io/en/stable/#table-configuration-and-options

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

@app.route('/api/products_v2', methods = ('GET', 'POST'))
def api_products_v2():

    draw = request.form['draw'] # "счетчик" +1 при новом запросе
    row = int(request.form['start']) # номер начальной строки
    rowperpage = int(request.form['length']) # количество выводимых строк
    searchValue = request.form["search[value]"] # строка для поиска

    pq = Product.query.offset(row).limit(rowperpage)
    if searchValue != '':
        pass
        # pq.like

        # print(request.form.columns)

    print(searchValue)
    return {'data': [product.to_dict() for product in pq]}
