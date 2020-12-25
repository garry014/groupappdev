from flask import Flask, render_template, request, redirect, url_for, Request
from Forms import *
import os
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = './static/uploads/ads/'
app.config['MAX_CONTENT_LENGTH'] = 0.1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    error = None
    create_ad = CreateAd(request.form)
    if request.method == 'POST' and create_ad.validate():
        if (create_ad.startdate.data > create_ad.enddate.data): #Compare start and end dates.
            error = "End date cannot be earlier than start date"
        else:
            print("This is running")
            if 'image' not in request.files:
                error = 'Something went wrong.'
            file = request.files['image']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                error = 'Please upload a file.'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                directlink = 'uploads/ads/'+filename
                os.rename('static/uploads/ads/'+filename, 'static/uploads/ads/'+'7.jpg')
                return redirect(url_for('static', filename=directlink))
            #return redirect(url_for('manage_ads'))
    return render_template('advertise.html', form=create_ad, error = error)

#ERROR 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#ERROR 413: File size is too big
@app.errorhandler(413)
def error413(e):
    return render_template('404.html'), 413

if __name__ == '__main__':
    app.debug = True
    app.run()