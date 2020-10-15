from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired
from flaskr.models.Clients import Client

class ClientForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    passport_number = StringField('PassportNumber', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()],format='%Y-%m-%d')
    deathday = DateField('Deathday', validators=[DataRequired()],format='%Y-%m-%d')
    size = StringField('Size', validators=[DataRequired()])
    weight = DecimalField('Weight', validators=[DataRequired()])
    cemeteries = SelectField("Cemeteries")
    mortuaries = SelectField("Mortuaries")
    id = HiddenField('Id');

    def __init__(self, client: Client = None, mortuaries_list: list = None, cemeteries_list: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if mortuaries_list:
            self.mortuaries.choices = mortuaries_list

        if cemeteries_list:
            self.cemeteries.choices = cemeteries_list

        if client is not None:
            self.id.data = client.client_id
            self.fullname.data = client.fullname
            self.passport_number.data = client.passport_number
            self.birthday.data = client.birthdate
            self.deathday.data = client.deathdate

            self.size.data = client.size
            self.weight.data = client.weight
            self.id = client.client_id

    submit = SubmitField('Create')