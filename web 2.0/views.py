from models import *

from flask import render_template, url_for, request

import json


@app.route('/', methods = ['post', 'get'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        obj = Object(name = name)
        db.session.add(obj)
        db.session.commit()

    return render_template('main.html', objects = Object.query)


@app.route('/object/<object_id>')
def object(object_id):
    object = Object.query.filter_by(id = object_id).one()
    # print(object)
    return render_template('object.html', object = object)

@app.route('/connection', methods = ['post', 'get'])
def connection():
    if request.method == 'POST':
        child_id = request.form.get('child_name')
        parent_id = request.form.get('parent_name')
        asts = Association(id_child = child_id, id_parent = parent_id)
        db.session.add(asts)
        db.session.commit()

    return render_template('connection.html',
        objects = Object.query,
        associations = Association.query)

@app.route('/object_smart_table', methods = ['post', 'get'])
def object_smart_table():
    objs = Object.query
    asocs = Association.query
    return render_template('object_smart_table.html', objs = objs)

@app.route('/connection_smart_table', methods = ['post', 'get'])
def connection_smart_table():
    objs = Object.query
    asocs = Association.query
    return render_template('connection_smart_table.html', asocs = asocs)

@app.route('/create_object', methods = ['POST', 'GET'])
def ajax_new_object():
    json_req = request.get_json()
    name = json_req['name']
    obj = Object(name = name)
    db.session.add(obj)
    db.session.commit()
    mes = json.dumps({
        'row_id': obj.id,
        'name': obj.name
    })
    return mes

@app.route('/update_object', methods = ['POST', 'GET'])
def ajax_update_object():
    json_req = request.get_json()
    name = json_req['name']
    object_id = json_req['row_id']

    obj = Object.query.filter_by(id = object_id).one()
    obj.name = name
    db.session.add(obj)
    db.session.commit()
    mes = json.dumps({
        'row_id': obj.id,
        'name': obj.name
    })
    return mes

@app.route('/delete_object', methods = ['POST', 'GET'])
def ajax_del_object():
    json_req = request.get_json()
    object_id = json_req['row_id']
    obj = Object.query.filter_by(id = object_id).one()
    db.session.delete(obj)
    db.session.commit()
    return '1'

@app.route('/test_page', methods = ['POST', 'GET'])
def test_page():
    return render_template('test_page.html')

if __name__ == '__main__':
    app.run()
