from flask import Flask

def create_app():
    app = Flask(__name__, template_folder = "templates")
    app.config['SECRET_KEY']='AASDFASDF'
    app.debug =  True
    # host= '0.0.0.0'

    # from . import flask_parser

    from flask_funcs import flask_app

    # from . import auth
    # app.register_blueprint(auth.bp)

    return app

# app = create_app()



app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY']='AASDFASDF'
app.debug =  True
# host= '0.0.0.0'

# from . import flask_parser

from flask_funcs import flask_app
