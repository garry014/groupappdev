from flask import Flask, render_template, request, redirect, url_for, Request
from Forms import *
import os, shelve, Ads
from datetime import date
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
                try:
                    db = shelve.open('ads.db', 'c')
                    ads_dict = db['Ads']
                except:
                    print("Error in opening DB")#return redirect(url_for('dberror'))

                try:
                    count_id = max(ads_dict, key=int) + 1
                except:
                    count_id = 1 #if no dictionary exist, set id as 1

                #Image Handling
                app.config['UPLOAD_FOLDER'] = './static/uploads/ads/'
                filename = secure_filename(file.filename)
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_extension = os.path.splitext(filename) # get file type
                os.rename('static/uploads/ads/'+filename, 'static/uploads/ads/'+ str(count_id) + file_extension[1])
                #End of Image Handling

                username = "Ah Tiong" #Testing username

                # Cost Calculation
                delta = create_ad.enddate.data - create_ad.startdate.data
                cost = delta.days * 25

                ad = Ads.Ads(str(count_id) + file_extension[1], username, create_ad.startdate.data,
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

@app.route('/manage_ads')
def manage_ads():
    ads_dict = {}
    username = "Admin" #Test Script
    try:
        db = shelve.open('ads.db', 'r')
        ads_dict = db['Ads']
        db.close()
    except:
        print("Db error")
    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)


    return render_template('manage_ads.html', count=len(ads_list), ads_list=ads_list, username=username)

@app.route('/updateAd/<int:id>/<int:updatewhat>/', methods=['GET', 'POST'])
def updateAd(id, updatewhat):
    update_ad = CreateAd(request.form)
    if updatewhat == 1:
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'w')
            ads_dict = db['Ads']
        except:
            return redirect(url_for('db_error'))
        ad = ads_dict.get(id)
        ad.set_status("Approved")
        db['Ads'] = ads_dict
        db.close()
        return redirect(url_for('manage_ads'))

    if request.method == 'POST' and update_ad.validate():
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'w')
            ads_dict = db['Ads']
        except:
            return redirect(url_for('db_error'))

        ad = ads_dict.get(id)
        ad.set_start_date(update_ad.startdate.data)
        ad.set_end_date(update_ad.enddate.data)

        db['Ads'] = ads_dict
        db.close()
        return redirect(url_for('manage_ads'))
    else:
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'r')
            ads_dict = db['Ads']
            db.close()
        except:
            return redirect(url_for('db_error'))

        ad = ads_dict.get(id)
        update_ad.startdate.data = ad.get_start_date()
        update_ad.enddate.data = ad.get_end_date()
    return render_template('updateAd.html', form=update_ad)

# @app.route('/updateAd/<int:id>/<str:updatewhat>', methods=['GET', 'POST'])
# def updateAdStatus(id, updatewhat):
#     print("this is running")
#     update_ad = CreateAd(request.form)
#     if request.method == 'POST' and update_ad.validate():
#         try:
#             ads_dict = {}
#             db = shelve.open('ads.db', 'w')
#             ads_dict = db['Ads']
#         except:
#             return redirect(url_for('db_error'))
#
#         if updatewhat == "status":
#             ad = ads_dict.get(id)
#             ad.set_status("Approved")
#
#         db['Ads'] = ads_dict
#         db.close()
#     return redirect(url_for('manage_ads'))

@app.route('/deleteAd/<int:id>', methods=['POST'])
def delete_ad(id):
    ads_dict = {}
    try:
        db = shelve.open('ads.db', 'w')
        ads_dict = db['Ads']
    except:
        return redirect(url_for('db_error'))
    else:
        for i in ALLOWED_EXTENSIONS:
            directpath = 'static/uploads/ads/'+ str(id) + '.' + i
            if os.path.exists(directpath):
                os.remove(directpath)
        ads_dict.pop(id)
        db['Ads'] = ads_dict
        if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
        db.close()
        return redirect(url_for('manage_ads'))

#ERROR 404 Not Found Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#ERROR 413: File size is too big
@app.errorhandler(413)
def error413(error):
    return render_template('413.html'), 413

#Database error
@app.route('/dberror')
def dberror():
    return render_template('dberror.html')

if __name__ == '__main__':
    app.debug = True
    app.run()