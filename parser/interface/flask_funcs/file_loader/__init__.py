from flask import Blueprint

bp = Blueprint('file_loader', __name__)

from flask_funcs.file_loader import excel_reader
