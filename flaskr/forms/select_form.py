from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired
from flaskr.models.Funerals import Funeral

class SelectForm(FlaskForm):

    select = SelectField("List")

    def __init__(self, label, select_list: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if select_list:
            self.select.choices = select_list
            self.select.label = label

    submit = SubmitField('Make')