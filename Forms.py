from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange

from datetime import datetime
from datetime import timedelta
def get_max_date(Days): #Set date to the max days a user can select.
    max_date = datetime.now() + timedelta(days=Days)
    max_date = max_date.strftime('%Y-%m-%d')
    return max_date

class CreateAd(Form):
    min_date = datetime.today().strftime('%Y-%m-%d')
    max_date = get_max_date(90)
    startdate = DateField('Start Date:*', render_kw={'min': min_date, 'max': max_date, 'value': min_date}, validators=[validators.DataRequired()]) #DateRange(min=min_date, max=get_max_date(30))
    enddate = DateField('End Date:*', render_kw={'min': min_date, 'max': max_date}, validators=[validators.DataRequired()])
