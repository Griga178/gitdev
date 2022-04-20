
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class Subject_adding_form(FlaskForm):
    name = StringField("Название пердмета: ", validators=[DataRequired()])
    submit = SubmitField("Отправить")

class Model_adding_form(FlaskForm):
    name = StringField("Название модели: ", validators=[DataRequired()])
    submit = SubmitField("Отправить")
