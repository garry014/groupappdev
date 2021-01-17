from wtforms import Form, StringField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import Regexp, Length, InputRequired


class RidersAccounts(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email',  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    phone_number = StringField('Phone Number', [Length(8), validators.DataRequired()])
    transport = SelectField('Transport', [validators.DataRequired()], choices=[('', 'Select'), ('Van/Car', 'Van/Car'), ('Motorcycle', 'Motorcycle'), ('Bicycle', 'Bicycle'), ('On Foot', 'On Foot')], default='')
    license_number = StringField('License No Eg. 123456789A', [validators.DataRequired(), Regexp('[0-9]{9}[A-Z]{1}')])
    password = StringField('Password (minimum eight characters, at least one letter, one number and one special character) ', [validators.DataRequired(), Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')])
