from flask import Flask, render_template, url_for, request, redirect
from Forms import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def contact_us():
    return render_template('index.html')

@app.route('/manage_ads.html')
def manage_ads():
    return render_template('manage_ads.html')

@app.route('/advertise', methods=['GET', 'POST'])
def advertise():
    create_ad = CreateAd(request.form)
<<<<<<< HEAD
    if request.method == 'POST' and create_ad.validate():
        if (create_ad.startdate.data > create_ad.enddate.data): #Compare start and end dates.
            error = "End date cannot be earlier than start date"
=======
    if request.method == 'POST' and create_ad.validate(): #
        print(create_ad.startdate.data)
        CreateAd().compare_dates()
        if (create_ad.startdate.data > create_ad.enddate.data):
            pass
>>>>>>> parent of b486dc6... wtform sucks
        else:
            print("This is running")
            return redirect(url_for('home'))

    return render_template('advertise.html', form=create_ad)

#ERROR 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)