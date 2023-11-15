from flask import Flask

app = Flask(__name__, template_folder = "templates")

app.config['SECRET_KEY'] = 'AASDFASDF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/zakupki2.db'

app.debug =  True
