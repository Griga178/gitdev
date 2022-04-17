from flask import Flask, render_template, request, redirect, url_for
import sys
sys.path.append('../')
from data_loader import load_pkl_file as load
from classes import Subject_ver_3, Subjects_category, Model_ver2

app = Flask(__name__, template_folder = "templates")
pickle_file_name = 'Models_Subjects_dict'

def show_subjects():
    print('FUNCS IS LAUNCH')
    try:
        load_dict = load(pickle_file_name)
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

@app.route('/subjects', methods = ('GET', 'POST'))
def subject_page():
    data = load(pickle_file_name)
    subj_set = data['Subjects']
    return render_template('subjects_page.html', subj_set = subj_set)

@app.route('/desript/<name>', methods = ('GET', 'POST'))
def subj_desript(name):
    data = load(pickle_file_name)
    subj_set = data['Subjects']
    for sub in subj_set:
        if name == sub.name:
            subj = sub.chars_description_dict(subj_set)
            break
    return render_template('subj_desript.html', subj = subj)
if __name__ == "__main__":

    #app.run(host= '0.0.0.0')
    app.run(debug = True)
