from settings import DATA_BASE_PATH
from flask_sqlalchemy import SQLAlchemy
from main import app


db = SQLAlchemy(app)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer(), primary_key=True)
    id_parent = db.Column(db.Integer(), db.ForeignKey('object.id'))
    id_child = db.Column(db.Integer(), db.ForeignKey('object.id'))

    parent = db.relationship("Object", foreign_keys = "Association.id_parent")
    child = db.relationship("Object", foreign_keys = "Association.id_child")


with app.app_context():
    db.create_all()
