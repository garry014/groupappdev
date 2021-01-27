from wtforms import Form, StringField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Regexp, Length


class TailorsAccount(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=100), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=100), validators.DataRequired()])
    store_name = StringField("Store Name", [validators.DataRequired()])
    address1 = StringField("Address Line 1", [validators.DataRequired()])
    address2 = StringField("Address Line 2", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    postal_code = StringField('Postal Code', [Length(6), validators.DataRequired()])
    email = EmailField('Email',  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    phone_number = StringField('Phone Number', [Length(8), validators.DataRequired()])
    password = StringField('Password (minimum eight characters, at least one letter, one number and one special character) ', [validators.DataRequired(), Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')])

