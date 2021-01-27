from wtforms import Form, StringField, TextAreaField, SelectField, BooleanField, FormField, FileField, validators
from wtforms.fields.html5 import DecimalField, DateTimeField
from wtforms.validators import *

class AddContentForm(Form):
    topic = StringField(
        "Topic Title" ,[validators.DataRequired()]
    )

    video = FileField(
        "Video"
    )