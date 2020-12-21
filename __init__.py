from flask import Flask, render_template, url_for, request, redirect
from Forms import createAd
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def contact_us():
    return render_template('index.html')

@app.route('/manage_ads.html')
def manage_ads():
    return render_template('manage_ads.html')

@app.route('/advertise', methods=['GET', 'POST'])
def advertise():
    if request.method == 'POST' and createAd.validate():
        if createAd().validate_on_submit():
            print("Pass")
    return render_template('advertise.html')

#ERROR 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)