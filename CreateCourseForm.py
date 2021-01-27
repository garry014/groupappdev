from wtforms import Form, StringField, TextAreaField, SelectField, BooleanField, FormField, FileField, validators
from wtforms.fields.html5 import DecimalField, DateTimeField
from wtforms.validators import *

class CreateCourseForm(Form):
    title = StringField(
        "Course Title" ,[validators.DataRequired()]
    )

    tailor = StringField(        #should be get name from when they made acct
        "Tailor" ,[validators.DataRequired()]
    )

    #video = FileField(
    #    "Course Video Content" ,[validators.Optional()]
    #)

    material = TextAreaField(
        "Materials Needed" ,[validators.DataRequired()]
    )

    language = SelectField(
        "Language" ,[validators.DataRequired()],
        choices=[("English", "English"), ("Chinese", "Chinese")]
    )

    livecourse = SelectField(
        "Day", [validators.DataRequired()],
        choices=[("Mondays","Mondays"), ("Tuesdays","Tuesdays"), ("Wednesdays","Wednesdays"), ("Thursdays","Thursdays"), ("Fridays","Fridays"), ("Saturdays","Saturdays"), ("Sundays","Sundays")]
    )

    note = TextAreaField(
        "Note" ,[validators.Optional()]
    )

    price = DecimalField(
        "Price" ,[validators.DataRequired()]
    )

    tbnail = FileField(
       "Course Image Thumbnail"
    )
