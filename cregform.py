from wtforms import Form, StringField, SelectField, PasswordField, validators
from wtforms.fields.html5 import EmailField, IntegerField

class createCust(Form):
    city = SelectField(
        "City", [validators.DataRequired()],
        choices=[("Singapore","Singapore")]
    )

    email = EmailField(
        "Email",[validators.required()]
    )
    password = PasswordField(
        "Password", [validators.required()]
    )
    firstname = StringField(
        "First Name", [validators.required()]
    )
    lastname = StringField(
        "Last Name", [validators.required()]
    )
    number = IntegerField(
        "Number", [validators.required()]
    )

