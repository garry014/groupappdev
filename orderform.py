from wtforms import Form, StringField, validators

class createOrder(Form):
    cname = StringField('Name', [validators.DataRequired()])
    description = StringField('Description', [validators.DataRequired()])
    price = StringField('Price', [validators.DataRequired()])
    due_date = StringField('Due Date', [validators.DataRequired()])


