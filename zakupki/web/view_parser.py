from .view_main_page import *


@app.route('/parse_page')
def get_parse_page():

    return render_template('parser.html', **parse_app.get_info())

@app.route('/get_sum_info', methods = ['GET'])
def get_sum_info():
    return parse_app.get_sum_info()

@app.route('/start_parse_numbers', methods = ['GET', 'POST'])
def start_parse_numbers():

    parse_app.set_dates(**request.form)
    # parse_app.app_status = 1
    return parse_app.get_info()

@app.route('/check_info', methods = ['GET'])
def check_info():
    return parse_app.get_info()
