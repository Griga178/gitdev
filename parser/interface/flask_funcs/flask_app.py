from flask import Flask, render_template, request, redirect, url_for, flash, json


import sys
sys.path.append('../')
from data_loader import load_pkl_file as load
from data_loader import save_pkl as save

from classes import Subject_ver_3, Subjects_category, Model_ver2
from input_form_classes import Subject_adding_form, Tags_form

from . import app

from back_end_manager import parse_one_link, manual_result_saving
from engine_data_base import show_list_shops, show_shop_sett, show_few_links_sql, delete_setting, take_post_message



pickle_file_name = 'Models_Subjects_dict'

def chose_model_example_by_name(name):
    search_model_example = False
    data = load(pickle_file_name)
    model_example_list = data['Models']
    for model_example in model_example_list:
        if model_example.name == name:
            search_model_example = model_example
            break
    return search_model_example

@app.route('/', methods = ('GET', 'POST'))
def index():
    return render_template('main.html')

@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    name = request.form['name'];
    return json.dumps({'len': len(name)})


# """ - - - ПАРСЕР - - -"""

# цена, название предмета, характеристики, статус
# список отпарсенных ссылок - скачать csv
# Отображение всех отпрсенных сайтов - главная страница # пагинация
@app.route('/parser')
def open_parser():
    return render_template('parser_pages/check_links.html')
# ВЫВОД СПИСКА МАГАЗИНОВ
@app.route('/print_links_base')
def print_links_base():
    dict_m_p = show_list_shops()
    return dict_m_p
# СМОТРИМ НАСТРОЙКИ ТЕГОВ
@app.route('/links_sett/<some_data>')
def links_sett(some_data):
    dict_m_p = show_shop_sett(some_data)
    return dict_m_p
# ПАРСИМ 1 НЕИЗВЕСТНУЮ ССЫЛКУ
@app.route('/parser_link_check', methods = ['GET', 'POST'])
def parse_link():
    json_message_new = parse_one_link(input_link = request.form['name'])
    return json_message_new
# ПАРСИМ 1 ИЗВЕСТНУЮ ССЫЛКУ
@app.route('/parse_one_links/<net_link_id>')
def parse_one_links(net_link_id):
    json_message_new = parse_one_link(input_id = net_link_id)
    return json_message_new
# СОХРАНЯЕМ РЕЗУЛТАТЫ ПАРСИНГА
@app.route('/send_parse_result', methods = ['GET', 'POST'])
def send_parse_resalt():
    if request.method == "POST":
        print("Сохранеяем")
        dict_to_db = request.form.to_dict()
        save_result = manual_result_saving(dict_to_db)
        return save_result

@app.route('/save_sett/<string_data>', methods = ['GET', 'POST'])
def save_sett(string_data):
    py_response = take_post_message(string_data)
    return py_response

@app.route('/del_sett/<string_data>', methods=['GET', 'POST'])
def del_sett(string_data):
    py_response = delete_setting(string_data)
    return py_response

# ПАРСИМ ФАЙЛ С СЫЛКАМИ
@app.route('/file_parser', methods=['GET', 'POST'])
def file_parser():
    return render_template('parser_pages/file_parser.html')

@app.route('/show_few_links/<shop_id>')
def show_few_links(shop_id):
    links_dict = show_few_links_sql(shop_id)
    return links_dict

# """ - - - БАЗЫ ДАННЫХ - - -"""

@app.route('/data', methods = ('GET', 'POST'))
def manage_data():
    return render_template('data_base.html')

# ПРЕДМЕТЫ
# Главная по предметам (добавить новый предмет)
@app.route('/subjects', methods = ('GET', 'POST'))
def subject_page():
    data = load(pickle_file_name)
    subj_set = data['Subjects']
    if request.method == 'POST':
        subj_name = request.form['subject_name']
        if len(subj_name) > 0:
            subj_set.add(Subject_ver_3(subj_name))
            save(data, pickle_file_name)
    subj_list = list(subj_set)
    subj_list.sort(key=lambda x: x.name)
    return render_template('subjects_page.html', subj_set = subj_list)

# Удалить предмет
@app.route('/subjects/<sub_name>', methods = ('GET', 'POST'))
def subject_del(sub_name):
    data = load(pickle_file_name)
    subj_set = data['Subjects']
    for subs in subj_set:
        if sub_name == subs.name:
            sub_example = subs
            subj_set.remove(sub_example)
            save(data, pickle_file_name)
            break
    return subject_page()
# Описание предмета
@app.route('/subjects/desript/<name>', methods = ('GET', 'POST'))
def subj_desript(name):
    data = load(pickle_file_name)
    subj_set = data['Subjects']
    models_list = list(data['Models'])
    models_list.sort(key=lambda x: x.name)
    for sub in subj_set:
        if name == sub.name:
            subject_example = sub
            subj = subject_example.chars_description_dict(subj_set)

            subj_models = sub.show_model()
            break
    # Добавить модель
    if request.method == 'POST':
        subj_model_name = request.form['model_name']
        print(f'Добавляем МОДЕЛЬ: {subj_model_name}')
        subj_model_example = chose_model_example_by_name(subj_model_name)
        print(f': В ЭКЗЕМЛЯР: {subject_example}')
        subject_example.add_models(subj_model_name, subj_model_example)
        save(data, pickle_file_name)
        # if len(subj_name) > 0:
        #     subj_set.add(Subject_ver_3(subj_name))
        #     save(data, pickle_file_name)

    return render_template('subj_desript.html', subj = subj, subj_models = subj_models, models_list = models_list)


# МОДЕЛИ
@app.route('/models', methods = ('GET', 'POST'))
def models_form():
    load_dict = load(pickle_file_name)
    if request.method == 'POST':
        mod_name = request.form['model_name']
        load_dict['Models'].add(Model_ver2(mod_name))
        save(load_dict, pickle_file_name)
    models_list = list(load_dict['Models'])
    models_list.sort(key=lambda x: x.name)
    return render_template('models_form.html', mod_set = models_list)

# Удалить предмет
@app.route('/models/<model_name>', methods = ('GET', 'POST'))
def model_del(model_name):
    data = load(pickle_file_name)
    models_set = data['Models']
    for model in models_set:
        if model_name == model.name:
            model_example = model
            models_set.remove(model_example)
            save(data, pickle_file_name)
            break
    return models_form()

# Описание и изменение 1 модели
# Модель:
#     name if Название предмета - изменить* else Добавить предмет
#     список характеристик - изменить*
#     Добавить характеристику, значение, ед.изм
@app.route('/models/information/<model_str_name>', methods = ('GET', 'POST'))
def model_information(model_str_name):
    model_example = chose_model_example_by_name(model_str_name)
    model_dict_description = model_example.full_description_dict()
    if request.method == "POST":
        print(request.form)
        # char, ch_val, ch_mes = request.form['char_name'], request.form['char_value'], request.form['char_measure']
        # print(char, ch_val, ch_mes)
        # if request.form['input_subject_name']:
        #     input_subject_name = request.form['input_subject_name']
        #     print(input_subject_name)
    return render_template('model_information.html', model_example = model_example, descript = model_dict_description)

@app.route('/settings', methods = ('GET', 'POST'))
def set_all():
    form = Subject_adding_form()

    if form.validate_on_submit():
        name = form.name.data
        # здесь логика базы данных
        print(f"\nData received. Now redirecting ...{name}")
        flash(f'Предмет: "{name}" добавлен успешно')
        print(type(name))
        return redirect(url_for('set_all'))
    else:
        print("В форму не попали")


    return render_template('settings.html', form = form)

# if __name__ == "__main__":
    #app.run(host= '0.0.0.0')

    # app.run(debug = True)
