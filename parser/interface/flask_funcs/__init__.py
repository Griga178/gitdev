from flask import Flask

# app = create_app()

UPLOAD_FOLDER = './flask_funcs/file_loader/upload_folder'

app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY']='AASDFASDF'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug =  True
# host= '0.0.0.0'

# from flask_funcs.file_loader import bp as file_loader_bp
# app.register_blueprint(file_loader_bp)


from flask_funcs import main_manager

from flask_funcs import module_data_base
from flask_funcs import module_parser

from flask_funcs import flask_app
