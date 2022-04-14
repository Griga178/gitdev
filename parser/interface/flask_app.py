from flask import Flask, render_template, request, redirect, url_for
import sys
sys.path.append('../')
from data_loader import load_pkl_file as load
from classes import Subject_ver_3, Subjects_category, Model_ver2

app = Flask(__name__, template_folder = "templates")


def show_subjects():
    print('FUNCS IS LAUNCH')
    try:
        load_dict = load('Models_Subjects_dict')
        print('\n')
        print(load_dict)
        print('\n')
    except:
        print('Не загрузить!')
        load_dict['Subjects'] = {'1', '2'}
    return load_dict['Subjects']


@app.route('/', methods = ('GET', 'POST'))
def index():
    return render_template('main.html')

@app.route('/data', methods = ('GET', 'POST'))
def manage_data(data = False):
    if data == 'Subjects':
        print('122123123123123123')
        loaded_data = show_subjects()
    else:
        print(data)
        loaded_data = {'no', 'yo', 'yo1'}
    return render_template('data_base.html', data = loaded_data)

if __name__ == "__main__":

    #app.run(host= '0.0.0.0')
    app.run(debug = True)
