import re
import os
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, FileField, validators
from wtforms.fields.html5 import DateField

from datetime import datetime
from datetime import timedelta
def get_today(): #Get today's date
    return datetime.today().strftime('%Y-%m-%d')

def get_max_date(Days): #Get the date to the max days a user can select.
    max_date = datetime.now() + timedelta(days=Days)
    max_date = max_date.strftime('%Y-%m-%d')
    return max_date

class CreateAd(Form):
    min_date = get_today()
    max_date = get_max_date(90)
    startdate = DateField('Start Date:*', render_kw={'min': min_date, 'max': max_date, 'value': min_date}, validators=[validators.DataRequired()])
    enddate = DateField('End Date:*', render_kw={'min': min_date, 'max': max_date}, validators=[validators.DataRequired()])
    #Changes
    image = FileField('Advertisement Image (capped at 16MB):*')

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)