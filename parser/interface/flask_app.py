from flask import Flask, render_template, request, redirect, url_for
import sys
sys.path.append('../')
from data_loader import load_pkl_file as load
from data_loader import save_pkl as save
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
def manage_data():

    return render_template('data_base.html')

@app.route('/forms_subj', methods = ('GET', 'POST'))
def subjects_form():
    load_subjects = load(pickle_file_name)
    if request.method == 'POST':
        subj_name = request.form['subject_name']
        load_subjects['Subjects'].add(Subject_ver_3(subj_name))
        save(load_subjects, pickle_file_name)
        print(f'{subj_name} добавлен')
    return render_template('subjects_form.html', subj_set = load_subjects['Subjects'])

@app.route('/forms_mod', methods = ('GET', 'POST'))
def models_form():
    load_dict = load(pickle_file_name)
    if request.method == 'POST':
        mod_name = request.form['model_name']
        load_dict['Models'].add(Model_ver2(mod_name))
        save(load_dict, pickle_file_name)
    return render_template('models_form.html', mod_set = load_dict['Models'])


@app.route('/descript/<sub_name>')
def sub_descript(sub_name):
    load_dict = load(pickle_file_name)
    load_set = load_dict['Subjects']
    data = False
    for subj in load_set:
        if sub_name == subj.name:

            data = subj.chars_description(load_set)
            break
    if not data:
        data = 'Не загрузилось'

    return render_template('subject_description.html', data = data)

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
