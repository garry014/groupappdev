from wtforms import Form, StringField, TextAreaField, SelectField, BooleanField, FormField, FileField, validators
from wtforms.fields.html5 import DecimalField, DateTimeField
from wtforms.validators import *

class CreateCourseForm(Form):
    title = StringField(
        "Course Title*" ,[validators.DataRequired(message="Please fill in your title.")]
    )


    material = TextAreaField(
        "Materials Needed*" ,[validators.DataRequired(message="Please fill the materials needed for the course.")]
    )

    language = SelectField(
        "Language*" ,[validators.DataRequired()],
        choices=[("English", "English"), ("Chinese", "Chinese")]
    )

    livecourse = SelectField(
        "Day*", [validators.DataRequired()],
        choices=[("Mondays","Mondays"), ("Tuesdays","Tuesdays"), ("Wednesdays","Wednesdays"), ("Thursdays","Thursdays"), ("Fridays","Fridays"), ("Saturdays","Saturdays"), ("Sundays","Sundays")]
    )

    note = TextAreaField(
        "Note" ,[validators.Optional()]
    )

    price = DecimalField(
        "Price*" ,[validators.DataRequired(message="Price must be between $1 and $500 only."), validators.NumberRange(min=1, max=500)],
    )

    tbnail = FileField(
       "Course Image Thumbnail*"
    )
