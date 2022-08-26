from flask import render_template, request, redirect, url_for, flash, json

from . import app

from flask_funcs.main_manager import parse_from_input, parse_from_registered_link

from flask_funcs.main_manager import get_shop_list
from flask_funcs.main_manager import get_shop_setting
from flask_funcs.main_manager import delete_set_by_id, update_tag_setting, save_shop_setting

# для базы данных
from flask_funcs.main_manager import get_table_links

from flask_funcs.main_manager import file_recept
# from engine_data_base import delete_setting, take_post_message

@app.route('/', methods = ('GET', 'POST'))
def index():
    return render_template('main.html')

# @app.route('/get_len', methods=['GET', 'POST'])
# def get_len():
#     name = request.form['name'];
#     return json.dumps({'len': len(name)})


# """ - * - * - * - * - * - * - * - * - * - * - * - * - Настроки Парсера - * - * - * - * - * - * - * - * - * - * - * - * -"""
@app.route('/parser')
def open_parser_setting():
    return render_template('parser_setting.html')

@app.route('/select_shops')
def print_links_base():
    shop_list = get_shop_list()
    return shop_list

# ПАРСИМ 1 НЕИЗВЕСТНУЮ ССЫЛКУ (Добаваляем новую(ые) ссылку(и))
@app.route('/parser_link_check', methods = ['GET', 'POST'])
def parse_link():
    input_link = request.form['name']
    json_message_new = parse_from_input([input_link])
    return json_message_new

# ПАРСИМ 1 ИЗВЕСТНУЮ ССЫЛКУ
@app.route('/parse_one_links/<net_link_id>')
def parse_one_links(net_link_id):
    json_message_new = parse_from_registered_link([net_link_id])
    return json_message_new

@app.route('/get_shop_setting/<shop_id>')
def links_sett(shop_id):
    shop_setting = get_shop_setting(shop_id)
    return shop_setting

@app.route('/save_tag_setting', methods = ['GET', 'POST'])
def save_sett():
    dict_to_db = request.get_json()
    save_result = update_tag_setting(dict_to_db)
    return save_result

@app.route('/save_shop_setting', methods = ['GET', 'POST'])
def take_shop_setting():
    dict_to_db = request.get_json()
    print(dict_to_db)
    save_shop_setting(dict_to_db)
    return 'success'

@app.route('/del_sett/<setting_id>', methods = ['GET', 'POST'])
def del_sett(setting_id):
    py_response = delete_set_by_id(setting_id)
    return 'success'

@app.route('/show_few_links/<shop_id>')
def show_few_links(shop_id):
    links_dict = show_few_links_sql(shop_id)
    return links_dict

# """ - * - * - * - * - * - * - * - * - * - * - * - * - Загрузка файлов - * - * - * - * - * - * - * - * - * - * - * - * -"""
@app.route('/file_loader', methods = ['GET', 'POST'])
def file_loader():
    return render_template('file_parser.html')

@app.route('/load_file', methods = ['GET', 'POST'])
def load_file():
    file = request.files.get('file')
    answer = file_recept(file, app)
    return answer

@app.route('/show_content', methods = ['GET', 'POST'])
def show_content():
    pass

@app.route('/parse_file', methods = ['GET', 'POST'])
def parse_file():
    pass

# """ - * - * - * - * - * - * - * - * - * - * - * - * - БАЗЫ ДАННЫХ - * - * - * - * - * - * - * - * - * - * - * - * -"""
@app.route('/data', methods = ('GET', 'POST'))
def manage_data():
    return render_template('data_base.html')

# ССЫЛКИ
@app.route('/links', methods = ['GET'])
def get_links():
    answer = get_table_links()
    # answer = 'ЭТО ИНФА С ССЫЛКАМИ'
    return answer

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
