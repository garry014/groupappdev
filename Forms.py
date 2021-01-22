from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, FileField, DecimalField, IntegerField, FieldList, BooleanField, validators
from wtforms.fields.html5 import DateField

from datetime import datetime
from datetime import timedelta
def get_today(): #Get today's date
    return datetime.today().strftime('%Y-%m-%d')

def get_tommorrow():
    tmr = datetime.now() + timedelta(days=1)
    tmr = tmr.strftime('%Y-%m-%d')
    return tmr

def get_max_date(Days): #Get the date to the max days a user can select. Have to feed in number of days.
    max_date = datetime.now() + timedelta(days=Days)
    max_date = max_date.strftime('%Y-%m-%d')
    return max_date

class CreateAd(Form):
    min_date = get_tommorrow()
    max_date = get_max_date(90)
    startdate = DateField('Start Date:*', render_kw={'min': min_date, 'max': max_date, 'value': min_date}, validators=[validators.DataRequired()])
    enddate = DateField('End Date:*', render_kw={'min': min_date, 'max': max_date}, validators=[validators.DataRequired()])
    image = FileField('Advertisement Image (capped at 16MB):*')
    adtext = StringField('Advertisement Text: (capped at 30 characters/optional)', [validators.Length(max=30)])

class UpdateAd(CreateAd):
    status = SelectField('', choices=[('Rejected', 'Rejected'), ('Approved', 'Approved'), ('Expired', 'Expired')])

class CreateProduct(Form):
    name = StringField('Name:*', [validators.Length(min=5, max=150), validators.DataRequired()])
    price = DecimalField('Price:* (Exclude $ sign)')
    image = FileField('Image:*')
    discount = IntegerField("Discounts:* (0 for N.A)")
    description = TextAreaField('Description:')
    q1 = StringField('Question 1:')
    q1category = RadioField('Category', [validators.DataRequired()], choices=[('textbox', 'Textbox - Open-ended question'), ('radiobtn', 'Radio Button - Single Choice Selection'), ('checkbox', 'Check boxes - Multiple Choice Selection')], default='textbox')
    flist1 = FieldList(StringField())
    # q2 = StringField('Question 1:')
    # q2category = RadioField('Category', [validators.DataRequired()],
    #                         choices=[('textbox', 'Textbox - Open-ended field for customer'),
    #                                  ('radiobtn', 'Radio Button - Single Choice Selection'),
    #                                  ('checkbox', 'Check boxes - Multiple Choice Selection')], default='')
    # flist2 = FieldList(StringField())

class SearchItem(Form):
    search = StringField('', render_kw={'placeholder': 'Store Name'})

class SendMsg(Form):
    message = StringField('', validators=[validators.DataRequired()])

class CreateChat(Form):
    message = TextAreaField('', validators=[validators.DataRequired()])
    email = StringField('') #validators.DataRequired(),

class CreateNoti(Form):
    message = StringField('', validators=[validators.DataRequired()])

class CreateReview(Form):
    stars = StringField('')
    review = TextAreaField('Leave a Review')
    photo = FileField('Photo:')