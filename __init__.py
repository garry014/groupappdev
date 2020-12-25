from flask import Flask, render_template, request, redirect, url_for, Request
from Forms import *
import os, shelve, Ads
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #File upload size cap 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def contact_us():
    return render_template('index.html')

@app.route('/advertise', methods=['GET', 'POST'])
def advertise():
    error = None
    create_ad = CreateAd(request.form)
    if request.method == 'POST' and create_ad.validate():
        if (create_ad.startdate.data > create_ad.enddate.data): #Compare start and end dates.
            error = "End date cannot be earlier than start date"
        else:
            if 'image' not in request.files:
                error = 'Something went wrong, please refresh page.'
            file = request.files['image']
            if file.filename == '':
                error = 'Please upload a file.'
            elif not allowed_file(file.filename):
                error = 'The file format must be in jpg, jpeg, png or gif.'
            elif file: #All validations done at this stage
                ads_dict = {}
                db = shelve.open('ads.db', 'c')

                try:
                    ads_dict = db['Ads']
                except:
                    print("Error in retrieving Ads from storage.db.")

                count_id = len(ads_dict) + 1

                #Image Handling
                app.config['UPLOAD_FOLDER'] = './static/uploads/ads/'
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_extension = os.path.splitext(filename) # get file type
                os.rename('static/uploads/ads/'+filename, 'static/uploads/ads/'+ str(count_id) + file_extension[1])
                #End of Image Handling

                username = "TailorNow" #Testing username

                ad = Ads.Ads(str(count_id) + file_extension[1], create_ad.startdate.data,
                               create_ad.enddate.data)
                ad.set_ad_id(count_id)
                ads_dict[ad.get_ad_id()] = ad
                db['Ads'] = ads_dict
                # Test codes
                ad = ads_dict[ad.get_ad_id()]

                db.close()

                return redirect(url_for('manage_ads'))
                #return redirect(url_for('static', filename=backoflink))
    return render_template('advertise.html', form=create_ad, error = error)

@app.route('/manage_ads.html')
def manage_ads():
    ads_dict = {}
    try:
        db = shelve.open('ads.db', 'r')
        ads_dict = db['Ads']
        db.close()
    except:
        print("Unable to open ads.db")

    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)
    #test code
    for ad in ads_list:
        print(ad.get_ad_id())
    return render_template('manage_ads.html', count=len(ads_list), ads_list=ads_list)

#ERROR 404 Not Found Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#ERROR 413: File size is too big
@app.errorhandler(413)
def error413(error):
    return render_template('413.html'), 413

if __name__ == '__main__':
    app.debug = True
    app.run()