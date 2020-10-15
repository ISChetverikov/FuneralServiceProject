from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired
from flaskr.models.Funerals import Funeral

class FuneralForm(FlaskForm):

    status = StringField('Status', validators=[DataRequired()])
    date = DateField('date', validators=[DataRequired()],format='%Y-%m-%d')
    cemeteries = SelectField("Cemeteries")
    clients = SelectField("Client")
    id = HiddenField('Id');

    def __init__(self, funeral: Funeral = None, client_list: list = None, cemeteries_list: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if client_list:
            self.clients.choices = client_list

        if cemeteries_list:
            self.cemeteries.choices = cemeteries_list

        if funeral is not None:
            self.id.data = funeral.funeral_id
            self.status.data = funeral.status
            self.date.data = funeral.date

    submit = SubmitField('Create')