from flask import Flask

app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY']='AASDFASDF'
app.debug =  True
# host= '0.0.0.0'


from flask_funcs import flask_app
