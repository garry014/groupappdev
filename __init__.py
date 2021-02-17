from flask import Flask, render_template, request, redirect, url_for, Request, session

from Delivery_Form import Deliver_Options
from Register_Customer import Customer_Register
from Forms import *
from cregform import *
from orderform import *
from targetform import *
from availform import *
from vform import *
import os, pathlib, re, shelve, Ads, CustRegister, Catalogue, Chat, Notification, Reviews, Orders, Target, Availability, Customer, Vouchers
from datetime import datetime as dt
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_COURSE_EXTENSION = {'mp4', 'mov'}

from Admin_Update_Form_Riders import UpdateAdmin
from Register_Form import CreateUserForm
from Forms_Riders import RidersAccounts
import Rider
from Admin_Update_Form_Tailors import AdminUpdateTailor
from Forms_Tailors import TailorsAccount
username = "Ah Tong Tailor"  #Test Script
import shelve, Tailor
from Register_Tailors import *
from Forms_Customers import *

from CreateCourseForm import *
from AddContentForm import *
import Course, Content, Cart


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024 #File upload size cap 1GB
courseCart ={}

@app.route('/')
def starting_page():
    return render_template('main_selection.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_course_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_COURSE_EXTENSION


# Get LOGIN-ed user details using session. Need to pass in type(customer,tailor, rider)
def get_userdata(usertype):
    db_dict = {}
    userdata = ""
    try:
        if usertype == "tailor":
            db = shelve.open('tailor_storage.db', 'r')
            db_dict = db['Tailors']
            userdata = db_dict.get(session['tailor_account'])
            db.close()
        elif usertype == "customer":
            db = shelve.open('customer.db', 'r')
            db_dict = db['Customer']
            userdata = db_dict.get(session['customer_account'])
            db.close()
        elif usertype == "rider":
            db = shelve.open('storage.db', 'r')
            db_dict = db['Users']
            userdata = db_dict.get(session['rider_account'])
            db.close()
    except:
        return redirect(url_for('general_error', errorid=0))
    else:
        return userdata

# Get user details of OTHER USERS. Need to pass in type(customer,tailor, rider), userid
def get_otheruserdata(usertype, userid):
    db_dict = {}
    userdata = ""
    try:
        if usertype == "tailor":
            db = shelve.open('tailor_storage.db', 'r')
            db_dict = db['Tailors']
            userdata = db_dict.get(userid)
            db.close()
        elif usertype == "customer":
            db = shelve.open('customer.db', 'r')
            db_dict = db['Customer']
            userdata = db_dict.get(userid)
            db.close()
        elif usertype == "rider":
            db = shelve.open('storage.db', 'r')
            db_dict = db['Users']
            userdata = db_dict.get(userid)
            db.close()
    except:
        return redirect(url_for('general_error', errorid=0))
    else:
        return userdata


def convert_store_username(storename):
    db_dict = {}
    try:
        db2 = shelve.open('tailor_storage.db', 'r')
        db_dict = db2['Tailors']
        db2.close()
    except:
        return redirect(url_for('general_error', errorid=0))
    print(storename)
    print(db_dict)

    tailor_username = ""
    for i in db_dict:
        if storename == db_dict[i].get_store_name():
            print("HERE")
            tailor_username = db_dict[i].get_user_name()
            print(tailor_username)
            break

    return tailor_username

################################ GARY'S CODE ###########################################
def view_notification():
    noti_dict = {}
    count = 0
    try:
        db = shelve.open('notification.db', 'r')
        noti_dict = db['Notification']
        db.close()
    except:
        return "down", count
    else:
        my_noti = {}

        for key,values in noti_dict.items():
            if session.get('customer_identity') is not None and values.get_recipient() == session['customer_identity']:
                my_noti[key] = values
                if values.get_status() == "new":
                    count += 1
            elif session.get('tailor_identity') is not None and values.get_recipient() == session['tailor_identity']:
                my_noti[key] = values
                if values.get_status() == "new":
                    count += 1
            elif session.get('rider_identity') is not None and values.get_recipient() == session['rider_identity']:
                my_noti[key] = values
                if values.get_status() == "new":
                    count += 1

        rev_dict = {}
        for i in sorted(my_noti.keys(), reverse=True):
            rev_dict[i] = my_noti[i]
        return rev_dict, count

app.jinja_env.globals.update(view_notification=view_notification)

def create_notification(recipient, category, message, hyperlink):
    noti_dict = {}
    try:
        db1 = shelve.open('notification.db', 'c')
        noti_dict = db1['Notification']
    except:
        print("Internal error of opening database.")

    try:
        count_id = max(noti_dict, key=int) + 1
    except:
        count_id = 1  # if no dictionary exist, set id as 1

    noti = Notification.Notification(recipient, category, message, hyperlink)
    noti.set_id(count_id)
    noti_dict[count_id] = noti
    db1['Notification'] = noti_dict

    db1.close()

@app.route('/noti/<action>/<int:id>', methods=['GET', 'POST'])
def update_notification(action,id):
    noti_dict = {}
    try:
        db1 = shelve.open('notification.db', 'w')
        noti_dict = db1['Notification']
    except:
        print("Database error")
    else:
        if action == "delete":
            if session.get('customer_identity') is not None and noti_dict[id].get_recipient() == session['customer_identity']:
                noti_dict.pop(id)
            elif session.get('tailor_identity') is not None and noti_dict[id].get_recipient() == session['tailor_identity']:
                noti_dict.pop(id)
            elif session.get('rider_identity') is not None and noti_dict[id].get_recipient() == session['rider_identity']:
                noti_dict.pop(id)
        if action == "readall":
            for noti in noti_dict:
                if session.get('customer_identity') is not None and noti_dict[noti].get_recipient() == session['customer_identity']:
                    noti_dict[noti].set_status("read")
                elif session.get('tailor_identity') is not None and noti_dict[noti].get_recipient() == session['tailor_identity']:
                    noti_dict[noti].set_status("read")
                elif session.get('rider_identity') is not None and noti_dict[noti].get_recipient() == session['rider_identity']:
                    noti_dict[noti].set_status("read")
        if action == "seeall":
            for noti in noti_dict:
                if session.get('customer_identity') is not None and noti_dict[noti].get_recipient() == session['customer_identity']:
                    noti_dict[noti].set_status("read")
                elif session.get('tailor_identity') is not None and noti_dict[noti].get_recipient() == session['tailor_identity']:
                    noti_dict[noti].set_status("read")
                elif session.get('rider_identity') is not None and noti_dict[noti].get_recipient() == session['rider_identity']:
                    noti_dict[noti].set_status("read")
            return redirect(url_for('all_notifications'))

        db1['Notification'] = noti_dict
        db1.close()
    return redirect(request.referrer)

@app.route('/all_notifications')
def all_notifications():
    return render_template('all_notifications.html')

@app.route('/cust_home')
def home():
    return redirect(url_for('home_page'))

@app.route('/index.html')
def home_page():
    try:
        ads_dict = {}
        db = shelve.open('ads.db', 'r')
        ads_dict = db['Ads']
        db.close()
    except:
        return redirect(url_for('general_error'), errorid=0)

    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)

    show_ads_list = []
    datetoday = datetime.today().strftime('%Y-%m-%d') #datetoday = datetime.today().strftime('%Y-%m-%d')
    datetoday = dt.strptime(datetoday, "%Y-%m-%d")
    print("date today;",datetoday)
    print(type(datetoday))

    for ad in ads_list:
        startdate_str = str(ad.get_start_date())
        enddate_str = str(ad.get_end_date())
        startdate = dt.strptime(startdate_str, "%Y-%m-%d")
        print(startdate_str, enddate_str, ad.get_status())
        enddate = dt.strptime(enddate_str, "%Y-%m-%d")
        datenow_str = str(datetime.now())

        #datenow = dt.strptime(datenow_str, "%Y-%m-%d")
        if (datetoday >= startdate) and (datetoday <= enddate) and ad.get_status() == "Approved": #enddate >= datetime.now()
            show_ads_list.append(ad)
            print(ad.get_store_name())

    return render_template('index.html', show_ads_list=show_ads_list)

@app.route('/advertise', methods=['GET', 'POST'])
def advertise():
    error = None
    create_ad = CreateAd(request.form)

    if session.get('tailor_identity') is None: #For restricted functions.
        return redirect(url_for('tailors_login'))

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
            # elif os.path.exists(file.filename): #if user deletes the file b4 submitting.
            #     error = 'The file you are submitting does not exist.'
            elif file: #All validations done at this stage
                ads_dict = {}
                try:
                    db = shelve.open('ads.db', 'c')
                    ads_dict = db['Ads']
                except:
                    error = "Internal error of opening database."

                try:
                    count_id = max(ads_dict, key=int) + 1
                except:
                    count_id = 1 #if no dictionary exist, set id as 1

                #Image Handling
                app.config['UPLOAD_FOLDER'] = './static/uploads/ads/'
                filename = secure_filename(file.filename)
                file_extension = os.path.splitext(filename)  # get file type
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1])):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1]))
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                os.rename('static/uploads/ads/'+filename, 'static/uploads/ads/'+ str(count_id) + file_extension[1])
                #End of Image Handling

                # Cost Calculation
                delta = create_ad.enddate.data - create_ad.startdate.data
                cost = delta.days * 25

                if(create_ad.adtext.data == None):
                    adtext = ' '
                else:
                    adtext = create_ad.adtext.data

                tailor_storename = "Admin Store Lah"
                if session['tailor_identity'] != "Admin":
                    tailor_storename = get_userdata("tailor").get_store_name()

                ad = Ads.Ads(str(count_id) + file_extension[1], tailor_storename, create_ad.startdate.data,
                               create_ad.enddate.data, adtext)
                ad.set_ad_id(count_id)
                ads_dict[ad.get_ad_id()] = ad
                db['Ads'] = ads_dict

                db.close()
                session["adpayment"] = cost
                return redirect(url_for('adpayment', id=ad.get_ad_id()))
                #return redirect(url_for('static', filename=backoflink))

    return render_template('advertise.html', form=create_ad, error=error)

@app.route('/adpayment/<int:id>', methods=['GET', 'POST'])
def adpayment(id):
    if session.get("adpayment") is None:
        return redirect(url_for('general_error', errorid=0))
    else:
        cost = session.get("adpayment")

    if request.method == 'POST':
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'w')
            ads_dict = db['Ads']
        except:
            return redirect(url_for('general_error', errorid=0))

        ad = ads_dict.get(id)
        ad.set_status("Pending Approval")
        db['Ads'] = ads_dict
        db.close()
        return redirect(url_for('manage_ads'))

    return render_template('adpayment.html', cost=cost)

@app.route('/manage_ads')
def manage_ads():
    if session.get('tailor_identity') is None: #For restricted functions.
        return redirect(url_for('tailors_login'))

    try:
        ads_dict = {}
        db = shelve.open('ads.db', 'w')
        ads_dict = db['Ads']
    except:
        return redirect(url_for('general_error', errorid=0))

    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)

    count = 0
    expired_list = []
    show_ads_list = []

    tailor_storename = ""
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    print("Logged in as:",session['tailor_identity']) #Test HEHE

    for ad in ads_list:
        if ad.get_store_name() == tailor_storename:
            count += 1
            show_ads_list.append(ad)
        enddate_str = str(ad.get_end_date())
        enddate = dt.strptime(enddate_str, "%Y-%m-%d")
        if enddate <= datetime.now() and ad.get_status() != "Rejected":
            expired_list.append(ad.get_ad_id())

    for id in expired_list:
        ad = ads_dict.get(id)
        ad.set_status("Expired")
        db['Ads'] = ads_dict
    db.close()

    if session['tailor_identity'] == "Admin":
        count = len(ads_list)
        show_ads_list = []
        show_ads_list = ads_list

    return render_template('manage_ads.html', count=count, ads_list=show_ads_list, username=username)

@app.route('/updateAd/<int:id>/<int:updatewhat>/', methods=['GET', 'POST'])
def updateAd(id, updatewhat):
    error = None
    update_ad = UpdateAd(request.form)

    if session.get('tailor_identity') is None: #For restricted functions.
        return redirect(url_for('tailors_login'))

    if updatewhat == 1 and session['tailor_identity'] == "Admin": #Update Status only
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'w')
            ads_dict = db['Ads']
        except:
            return redirect(url_for('general_error', errorid=0))
        ad = ads_dict.get(id)
        ad.set_status("Approved")

        tailor_username = convert_store_username(ad.get_store_name())

        create_notification(tailor_username,"updates","Your advertisement just got approved!", "manage_ads")  # create notification
        db['Ads'] = ads_dict
        db.close()

        return redirect(url_for('manage_ads'))
    else: #Update All
        if request.method == 'POST' and update_ad.validate():
            try:
                ads_dict = {}
                db = shelve.open('ads.db', 'w')
                ads_dict = db['Ads']
            except:
                return redirect(url_for('general_error', errorid=0))

            ad = ads_dict.get(id)
            ad.set_start_date(update_ad.startdate.data)
            ad.set_adtext(update_ad.adtext.data)
            if session['tailor_identity'] == "Admin":
                ad.set_status(update_ad.status.data)
                tailor_username = convert_store_username(ad.get_store_name())
                if update_ad.status.data == "Rejected":
                    create_notification(tailor_username, "updates", "Sorry, your advertisement isn't in-line with our terms and conditions and has been rejected.",
                                        "manage_ads")
                if update_ad.status.data == "Approved":
                    create_notification(tailor_username, "updates", "Your advertisement just got approved!",
                                        "manage_ads")
            else:
                ad.set_status("Pending Approval")

            if 'image' not in request.files:
                error = 'Something went wrong, please refresh page.'
            file = request.files['image']
            if file.filename != '' and not allowed_file(file.filename):
                error = 'The file format must be in jpg, jpeg, png or gif.'
            elif file: #All validations done at this stage
                # Image Handling
                app.config['UPLOAD_FOLDER'] = './static/uploads/ads/'
                filename = secure_filename(file.filename)
                oldfile = os.path.join(app.config['UPLOAD_FOLDER'], str(ad.get_image()))
                if os.path.exists(oldfile):
                    os.remove(oldfile)
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_extension = os.path.splitext(filename)  # get file type
                os.rename('static/uploads/ads/' + filename, 'static/uploads/ads/' + str(ad.get_ad_id()) + file_extension[1])
                ad.set_image(str(ad.get_ad_id()) + file_extension[1])
                # End of Image Handling

            #delta = update_ad.enddate.data - update_ad.startdate.data
            if (update_ad.enddate.data < update_ad.startdate.data):  # Compare start and end dates.
                error = "End date cannot be earlier than start date"
            else:
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
                return redirect(url_for('general_error', errorid=0))

            ad = ads_dict.get(id)

            if (session['tailor_identity'] != "Admin"):
                if (ad.get_store_name() != get_userdata("tailor").get_store_name()):
                    return redirect(url_for('general_error', errorid=1))

            update_ad.startdate.data = ad.get_start_date()
            update_ad.enddate.data = ad.get_end_date()
            update_ad.adtext.data = ad.get_adtext()
            if session['tailor_identity'] == "Admin":
                update_ad.status.data = ad.get_status()

        return render_template('updateAd.html', form=update_ad, username=username, erorr=error)

@app.route('/deleteAd/<int:id>', methods=['POST'])
def delete_ad(id):
    ads_dict = {}
    try:
        db = shelve.open('ads.db', 'w')
        ads_dict = db['Ads']
    except:
        return redirect(url_for('general_error', errorid=0))
    else:
        # test script
        storename_loginuser = get_otheruserdata("tailor", session['tailor_account'])

        if session.get('tailor_account') is None:  # For restricted functions.
            return redirect(url_for('tailors_login'))
        elif session['tailor_identity'] == "Admin" or session['tailor_account'].get_userdata().get_store_name() == ads_dict[id].get_store_name():
            print("HEHE")
            for i in ALLOWED_EXTENSIONS:
                directpath = 'static/uploads/ads/' + str(id) + '.' + i
                if os.path.exists(directpath):
                    os.remove(directpath)
            ads_dict.pop(id)
            db['Ads'] = ads_dict
            db.close()
            return redirect(url_for('manage_ads'))
        else:
            return redirect(url_for('general_error', errorid=1))

# @app.route('/CustRegister', methods=['GET', 'POST'])
# def createcustomeracct():
#     createcustacct = createCust(request.form)
#
#     if request.method == 'POST' and createcustacct.validate():
#         try:
#             custDict = {}
#             cdb = shelve.open('cust.db', 'c')
#             custDict = cdb['cust']
#         except:
#             print("error reading cust.db")
#
#         custacct = CustRegister.CustRegister(createcustacct.city.data, createcustacct.email.data,
#                                              createcustacct.password.data, createcustacct.firstname.data,
#                                              createcustacct.lastname.data, createcustacct.number.data)
#
#         cdb[createcustacct.email.data] = custacct
#         cdb['CustRegister'] = custDict
#
#         cdb.close()
#
#         return redirect(url_for('CustLogin'))
#
#     return render_template('CustRegister.html', form=createcustacct)

@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    create_prod = CreateProduct(request.form)
    error = None

    if session.get('tailor_account') is None:
        return redirect(url_for('tailors_login'))

    if request.method == 'POST' and create_prod.validate():
        if 'image' not in request.files:
            error = 'Something went wrong, please refresh page.'
        file = request.files['image']
        if file.filename == '':
            error = 'Please upload a file.'
        elif not allowed_file(file.filename):
            error = 'The file format must be in jpg, jpeg, png or gif.'
        # elif create_prod.q1.data != '' and create_prod.q1category.data != 'textbox':
        #     if len(create_prod.flist1.data) < 1:
        #         error = 'Please create at least one choice for each question.'
        elif file:  # All validations done at this stage
            catalogue_dict = {}
            try:
                db = shelve.open('catalogue.db', 'c')
                catalogue_dict = db['Catalogue']
            except:
                error = "Error in opening DB"

            tailor_storename = "Admin Store Lah"
            if session['tailor_identity'] != "Admin":
                tailor_storename = get_userdata("tailor").get_store_name()

            count_id = 0
            if tailor_storename in catalogue_dict: #Set count_id to the max number of the store
                for product in catalogue_dict[tailor_storename]:
                    if product.get_id() >= count_id:
                        count_id = product.get_id() + 1

            # Image Handling
            app.config['UPLOAD_FOLDER'] = './static/uploads/shops/' + tailor_storename + '/'
            filename = secure_filename(file.filename)
            pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True) #Create shop directory if does nt exist.
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)): #if upload filename exists
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_extension = os.path.splitext(filename)  # get file type
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1])):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1]))
            os.rename(app.config['UPLOAD_FOLDER'] + filename, app.config['UPLOAD_FOLDER'] +str(count_id) + file_extension[1])
            # End of Image Handling

            qns = ''
            if create_prod.q1.data != '':
                if create_prod.q1category.data == "radiobtn" and len(create_prod.flist1.data) > 1:
                    qns = Catalogue.Customiseable(create_prod.q1.data, create_prod.flist1.data, create_prod.q1category.data)
                elif create_prod.q1category.data == "textbox":
                    qns = Catalogue.Customiseable(create_prod.q1.data, None, create_prod.q1category.data)
                else:
                    error = "Please ensure all your customisable question fields is filled."

            if error == None:
                prod = Catalogue.Catalouge(count_id, create_prod.name.data, create_prod.price.data,
                                           create_prod.discount.data,
                                           str(count_id) + file_extension[1], create_prod.description.data, qns)

                if tailor_storename in catalogue_dict:
                    catalogue_dict[tailor_storename].append(prod)
                else:
                    catalogue_dict[tailor_storename] = [prod]

                db['Catalogue'] = catalogue_dict
                db.close()
                return redirect(url_for('catalogue'))


    return render_template('addproduct.html', form=create_prod, error=error)

@app.route('/catalogue')
def catalogue():
    if session.get('tailor_account') is None:
        return redirect(url_for('tailors_login'))

    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    tailor_storename = "Admin Store Lah"
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    if tailor_storename not in catalogue_dict:
        return redirect(url_for('add_product'))

    return render_template('catalogue.html', catalogue_list=catalogue_dict[tailor_storename], username=tailor_storename)

@app.route('/deleteProduct/<name>/<int:id>', methods=['POST'])
def delete_product(name, id):
    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'w')
        catalogue_dict = db['Catalogue']
    except:
        return redirect(url_for('general_error', errorid=0))
    else:
        for product in catalogue_dict[name]:
            if product.get_id() == id:
                catalogue_dict[name].remove(product)
                directpath = 'static/uploads/shops/' + name + '/' + product.get_image()
                if os.path.exists(directpath):
                    os.remove(directpath)
        db['Catalogue'] = catalogue_dict
        db.close()
        return redirect(url_for('catalogue'))

@app.route('/updateProduct/<name>/<int:id>', methods=['GET', 'POST'])
def updateProduct(name, id):
    update_prod = CreateProduct(request.form)
    error = None
    if request.method == 'POST' and update_prod.validate():
        try:
            catalogue_dict = {}
            db = shelve.open('catalogue.db', 'w')
            catalogue_dict = db['Catalogue']
        except:
            return redirect(url_for('general_error', errorid=0))
        for product in catalogue_dict[name]:
            if product.get_id() == id:
                product.set_name(update_prod.name.data)
                product.set_price(update_prod.price.data)
                product.set_discount(update_prod.discount.data)
                product.set_description(update_prod.description.data)
                qns = ''

                if update_prod.q1.data != '':
                    if update_prod.q1category.data == "radiobtn" and len(update_prod.flist1.data) > 1:
                        qns = Catalogue.Customiseable(update_prod.q1.data, update_prod.flist1.data,
                                                      update_prod.q1category.data)
                    elif update_prod.q1category.data == "textbox":
                        qns = Catalogue.Customiseable(update_prod.q1.data, None, update_prod.q1category.data)
                    else:
                        error = "Please ensure all your customisable question fields is filled."

                product.set_custom(qns)

                if 'image' not in request.files:
                    error = 'Something went wrong, please refresh page.'
                file = request.files['image']
                if file.filename != '' and not allowed_file(file.filename):
                    error = 'The file format must be in jpg, jpeg, png or gif.'
                elif file:  # All validations done at this stage
                    # Image Handling
                    app.config['UPLOAD_FOLDER'] = './static/uploads/shops/' + name + '/'
                    filename = secure_filename(file.filename)
                    oldfile = os.path.join(app.config['UPLOAD_FOLDER'], str(product.get_image()))
                    if os.path.exists(oldfile):
                        os.remove(oldfile)
                    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_extension = os.path.splitext(filename)  # get file type
                    os.rename(app.config['UPLOAD_FOLDER'] + filename,
                              app.config['UPLOAD_FOLDER'] + str(product.get_id()) + file_extension[1])
                    product.set_image(str(product.get_id()) + file_extension[1])
                    # End of Image Handling

                if error is None:
                    db['Catalogue'] = catalogue_dict
                    db.close()
                    return redirect(url_for('catalogue'))


    else:
        catalogue_dict = {}
        try:
            db = shelve.open('catalogue.db', 'r')
            catalogue_dict = db['Catalogue']
            db.close()
        except:
            return redirect(url_for('general_error', errorid=0))

        for product in catalogue_dict[name]:
            if product.get_id() == id:
                update_prod.name.data = product.get_name()
                update_prod.price.data = product.get_price()
                update_prod.discount.data = product.get_discount()
                update_prod.description.data = product.get_description()

                custom = product.get_custom()
                if custom != '':
                    update_prod.q1.data = custom.get_question()
                    update_prod.q1category.data = custom.get_category()


    return render_template('updateProduct.html', form=update_prod, error=error)

@app.route('/viewshops', methods=['GET' ,'POST'])
def view_shops():
    # to do my onchange checkbox, i nid to keep a copy of the data I have.
    error = None
    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    review_dict = {}
    try:
        db2 = shelve.open('review.db', 'r')
        review_dict = db2['Review']
        db2.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    tailor_dict = {}
    try:
        db3 = shelve.open('tailor_storage.db', 'r')
        tailor_dict = db3['Tailors']
        db3.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    # Get only store name and tailor_address
    address_dict = {}
    for key, value in tailor_dict.items():
        address_dict[value.get_store_name()] = [value.get_address1() + ' ' + value.get_address2(), value.get_city() + ' ' + value.get_postal_code()]

    shop_dict = {} #Key: [Total Review, Most Discounted Item]
    for key, value in catalogue_dict.items():
        total_review = 0
        best_disc = 0
        for item in value:
            total_review += item.get_reviews()
            if item.get_discount() > best_disc:
                best_disc = item.get_discount()
        shop_dict[key] = [total_review, best_disc]

    if request.method == 'POST':
        shop_dict = {}

        search = request.form.get('search')
        cbList = request.form.getlist('cbList')
        pricefilter = request.form.get('price')
        session['checkboxList'] = cbList

        pricefilter = re.findall(r'\d+', pricefilter)
        price1 = int(pricefilter[0])
        price2 = int(pricefilter[1])
        print(pricefilter)

        for key, value in catalogue_dict.items():
            best_disc = 0
            total_review = 0
            if search != '' and search.lower()[:5] == key.lower()[:5]:
                for item in value:
                    total_review += item.get_reviews()
                    if item.get_discount() > best_disc:
                        best_disc = item.get_discount()
                shop_dict[key] = [total_review, best_disc]

            if cbList:
                for item in value:
                    if "sales" in cbList:
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        if best_disc > 0:
                            shop_dict[key] = [total_review, best_disc]
                    if 'altering' in cbList and 'alter' in item.get_name().lower():
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        shop_dict[key] = [total_review, best_disc]
                    if 'tapering' in cbList and 'taper' in item.get_name().lower():
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        shop_dict[key] = [total_review, best_disc]
                    if 'suits' in cbList and 'customised suit' in item.get_name().lower():
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        shop_dict[key] = [total_review, best_disc]

            for item in value:
                if price1 != 6:
                    if item.get_price() >= price1 and item.get_price() <= price2:
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        shop_dict[key] = [total_review, best_disc]
                        print("show this", shop_dict)
                        break
                if price2 != 300:
                    if item.get_price() >= price1 and item.get_price() <= price2:
                        total_review += item.get_reviews()
                        if item.get_discount() > best_disc:
                            best_disc = item.get_discount()
                        shop_dict[key] = [total_review, best_disc]

        if not shop_dict: #Checks for empty dict
            error = "Sorry! We could not find the store you are looking for, try searching another store or changing your filter requirements."

        if search == '' and not cbList and (price1 == 6 and price2 == 300):
            return redirect(url_for('view_shops'))

        return render_template('viewshops.html', shop_dict=shop_dict, review_dict=review_dict, address_dict=address_dict, error=error)

    return render_template('viewshops.html', shop_dict=shop_dict, review_dict=review_dict, address_dict=address_dict, error=error)


@app.route('/view/<name>', methods=['GET', 'POST'])
def viewstore(name):
    catalogue_dict = {}
    disc_price_dict = {}
    createOrder = CreateOrder(request.form)
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error', errorid=0))
    #disc_price_dict[item.get_id()] = float(item.get_price()) * ((100 - float(item.get_discount()))/100) #Calculate item discount

    review_dict = {}

    try:
        db2 = shelve.open('review.db', 'r')
        review_dict = db2['Review']
        db2.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    if name not in catalogue_dict:
        return redirect(url_for('view_shops'))

    return render_template('viewstore.html', shop_dict=catalogue_dict[name], review_dict=review_dict, name=name, form=createOrder)

@app.route('/view/<name>/<int:productid>', methods=['GET', 'POST'])
def viewshopitem(name, productid):
    catalogue_dict = {}
    disc_price_dict = {}
    createOrder = CreateOrder(request.form)
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error'), errorid=0)
    #disc_price_dict[item.get_id()] = float(item.get_price()) * ((100 - float(item.get_discount()))/100) #Calculate item discount
    review_dict = {}

    try:
        db2 = shelve.open('review.db', 'r')
        review_dict = db2['Review']
        db2.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    if name not in catalogue_dict:
        return redirect(url_for('view_shops'))

    prod = None
    for product in catalogue_dict[name]:
        if productid == product.get_id():
            prod = product

    if prod is None:
        return redirect(url_for('general_error', errorid=2))

    # Amelia
    cart_dict = {}
    # session.pop('cart_session', None)
    # session.pop('cart_id', None)
    if session.get('cart_session') is None:
        session["cart_session"] = {}
        count_id = 1
    if session.get('cart_id') is None:
        session["cart_id"] = 0

    if request.method == "POST":
        req = request.form
        custom = req.get("custom")
        qty = req.get("qty")

        # Your fields validation please
        try:
            quantity = int(qty)
        except:
            print("Quantity not a valid integer")
        # End of validation #

        session["cart_id"] += 1

        shop_dict = catalogue_dict[name]
        productname = prod.get_name()
        unitprice = float(prod.get_price()) * (1-(prod.get_discount()/100))

        cart_id = str(session["cart_id"])
        # cart_dict = {cartitem_id(in str): [shop_name, productname, product_id, unitprice, quantity, custom]}
        cart_dict[cart_id] = [name, productname, productid, unitprice, quantity, custom]
        session["cart_session"].update(cart_dict)

    return render_template('viewshopitem.html', shop_dict=catalogue_dict[name], review_dict=review_dict, name=name, productid=productid, prod=prod, form=createOrder)

@app.route('/my_cart', methods=['GET', 'POST'])
def customer_cart():
    print(session["cart_session"])
    return render_template('customer_cart.html')


@app.route('/contact/<name>', methods=['GET', 'POST'])
def contact(name):
    username = None
    session.pop('temp_user', None)
    if session.get('customer_identity') is not None:
        username = session['customer_identity']
    elif session.get('temp_user') is not None:
        username = session['temp_user']
    elif session.get('tailor_identity') is not None:
        username = session['tailor_identity']
    elif session.get('rider_identity') is not None:
        username = session['rider_identity']

    create_chat = CreateChat(request.form)
    if request.method == 'POST' and create_chat.validate():
        chat_dict = {}
        try:
            db = shelve.open('chat.db', 'c')
            chat_dict = db['Chats']
        except:
            print("Internal error of opening database.")

        try:
            count_id = max(chat_dict, key=int) + 1
        except:
            count_id = 1  # if no dictionary exist, set id as 1

        msg_from = ""
        if username is not None:
            msg_from = username
        else:
            msg_from = create_chat.email.data
            session['temp_user'] = create_chat.email.data

        message = Chat.Message(create_chat.message.data, msg_from, dt.today().strftime("%d %b %Y %H:%M")) # | %A
        chat = Chat.Chat(count_id, msg_from, name)
        chat.set_messages(message)
        chat_dict[count_id] = chat


        db['Chats'] = chat_dict
        db.close()

        return redirect(url_for('chat_page', chat="inbox", chatid=count_id))
    return render_template('contact.html', form=create_chat, username=username)

@app.route('/<string:chat>/<int:chatid>', methods=['GET', 'POST'])
def chat_page(chat, chatid):
    send_msg = SendMsg(request.form)

    username = ""
    if session.get('customer_identity') is not None:
        username = session['customer_identity']
    elif session.get('temp_user') is not None:
        username = session['temp_user']
    elif session.get('tailor_identity') is not None:
        username = get_userdata("tailor").get_store_name()
    elif session.get('rider_identity') is not None:
        username = session['rider_identity']
    print(username)

    if request.method == 'POST':
        chat_dict = {}
        try:
            db = shelve.open('chat.db', 'w')
            chat_dict = db['Chats']
        except:
            return redirect(url_for('general_error'), errorid=0)

        if send_msg.validate():

            if session.get('customer_identity') is not None and chat_dict[chatid].get_sender() == session['customer_identity']:
                chat_dict[chatid].set_sender_status("Replied")
                chat_dict[chatid].set_recipient_status("Unreplied")
            else:
                chat_dict[chatid].set_sender_status("Unreplied")

            message = Chat.Message(send_msg.message.data, username, dt.today().strftime("%d %b %Y %H:%M"))
            chat_dict[chatid].set_messages(message)
        db['Chats'] = chat_dict
        db.close()

        return redirect(url_for('chat_page', chat="inbox", chatid=chatid))
    else:
        chat_dict = {}
        try:
            db = shelve.open('chat.db', 'r')
            chat_dict = db['Chats']
            db.close()
        except:
            return redirect(url_for('general_error'), errorid=0)

        user_chat = {}
        for item in chat_dict:
            if session.get('customer_identity') is None and session.get('temp_user') is not None:
                if chat_dict[item].get_sender() == session['temp_user']:
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            elif chat == "inbox":
                if chat_dict[item].get_sender() == username and chat_dict[item].get_sender_status() == "Hidden":
                    pass
                elif chat_dict[item].get_recipient() == username and chat_dict[item].get_recipient_status() == "Hidden":
                    pass
                elif chat_dict[item].get_sender() == username and chat_dict[item].get_sender_status() != "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
                elif chat_dict[item].get_recipient() == username and chat_dict[item].get_recipient_status() != "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            elif chat == "archive":
                if chat_dict[item].get_sender() == username and chat_dict[item].get_sender_status() == "Hidden":
                    pass
                elif chat_dict[item].get_recipient() == username and chat_dict[item].get_recipient_status() == "Hidden":
                    pass
                elif chat_dict[item].get_sender() == username and chat_dict[item].get_sender_status() == "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
                elif chat_dict[item].get_recipient() == username and chat_dict[item].get_recipient_status() == "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            else:
                return redirect(url_for('general_error', errorid=2))

        if username == "Admin":
            user_chat = chat_dict

    return render_template('chat.html', user_chat=user_chat, chatid=chatid, form=send_msg, username=username, chat=chat)

@app.route('/chat/<action>/<int:id>', methods=['GET', 'POST'])
def update_chatstatus(action, id):
    chat_dict = {}
    try:
        db = shelve.open('chat.db', 'w')
        chat_dict = db['Chats']
    except:
        return redirect(url_for('general_error'), errorid=0)
    else:
        username = ""
        if session.get('customer_identity') is not None:
            username = session['customer_identity']
        elif session.get('temp_user') is not None:
            username = session['temp_user']
        elif session.get('tailor_identity') is not None:
            username = get_userdata("tailor").get_store_name()
        elif session.get('rider_identity') is not None:
            username = session['rider_identity']
        print(username)

        if action == "resolved":
            chat_dict[id].set_recipient_status("Resolved")
        elif action == "delete":
            if username == "Admin":
                chat_dict.pop(id)
            elif username == chat_dict[id].get_recipient():
                chat_dict[id].set_recipient_status("Hidden")
            else:
                chat_dict[id].set_sender_status("Hidden")
        elif action == "archive":
            if username == chat_dict[id].get_recipient():
                chat_dict[id].set_recipient_status("Archive")
            else:
                chat_dict[id].set_sender_status("Archive")

        db['Chats'] = chat_dict
        db.close()

        if action != "archive":
            action = "inbox"
        return redirect(url_for('chat_page', chat=action ,chatid=id))


@app.route('/review/<shop>/<int:itemid>', methods=['GET' ,'POST'])
def review(shop, itemid):
    error = None
    product_name = ""
    createReview = CreateReview(request.form)

    if session.get('customer_identity') is None:
        return redirect(url_for('login_customers'))

    if request.method == 'POST':
        try:
            starsgiven = int(createReview.stars.data)
        except:
            error = 'Please rate with 1 to 5 stars.'
        else:
            file = request.files['photo']

            review_dict = {}
            try:
                db2 = shelve.open('review.db', 'c')
                review_dict = db2['Review']
            except:
                error = "Internal error opening database"

            try:
                count_id = max(review_dict, key=int) + 1
            except:
                count_id = 1  # if no dictionary exist, set id as 1

            if file.filename != '':
                if not allowed_file(file.filename):
                    error = 'The file format must be in jpg, jpeg, png or gif.'
                else:
                    # Image Handling
                    app.config['UPLOAD_FOLDER'] = './static/uploads/reviews/'
                    filename = secure_filename(file.filename)
                    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_extension = os.path.splitext(filename)  # get file type
                    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1])):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(count_id) + file_extension[1]))

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    os.rename('static/uploads/reviews/' + filename,
                              'static/uploads/reviews/' + str(count_id) + file_extension[1])
                    # End of Image Handling
                    thisreview = Reviews.Reviews(count_id, shop, itemid, session['customer_identity'], starsgiven, createReview.review.data,
                                                 str(count_id) + file_extension[1])
            else:
                thisreview = Reviews.Reviews(count_id, shop, itemid, session['customer_identity'], starsgiven, createReview.review.data, "")

            if error is None:
                review_dict[count_id] = thisreview
                db2['Review'] = review_dict
                db2.close()
                return redirect(url_for('viewshopitem', name=shop, productid=itemid))

    else:
        catalogue_dict = {}
        try:
            db = shelve.open('catalogue.db', 'r')
            catalogue_dict = db['Catalogue']
            db.close()
        except:
            return redirect(url_for('general_error'), errorid=0)

        nomatch = 1
        for key, value in catalogue_dict.items():
            if shop == key:
                for item in catalogue_dict[key]:
                    if item.get_id() == itemid:
                        product_name = item.get_name()
                        nomatch = 0
                        break

        if nomatch == 1:
            return redirect(url_for('general_error', errorid=2))
    return render_template('review.html', form=createReview, error=error, product_name=product_name)

@app.route('/viewReviews/<shop>/<int:productid>', methods=['GET' ,'POST'])
def viewReviews(shop, productid):
    review_dict = {}
    try:
        db2 = shelve.open('review.db', 'r')
        review_dict = db2['Review']
        db2.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    current_dict = {}
    for item in review_dict:
        if review_dict[item].get_storename() == shop and review_dict[item].get_productid() == productid:
            current_dict[item] = review_dict[item]
            print(current_dict) #Test script

    if not current_dict:
        return redirect(url_for('general_error', errorid=3))

    return render_template('viewReviews.html', current_dict=current_dict, username=username, productid=productid, shop=shop)

@app.route('/deleteReview/<shop>/<int:productid>/<int:id>', methods=['GET', 'POST'])
def deleteReview(shop, productid, id):
    review_dict = {}
    try:
        db2 = shelve.open('review.db', 'w')
        review_dict = db2['Review']
    except:
        return redirect(url_for('general_error', errorid=0))
    else:
        review_dict.pop(id)
        db2['Review'] = review_dict
        db2.close()
        return redirect(url_for('viewshopitem', name=shop, productid=productid))

@app.route('/updateReview/<shop>/<int:productid>/<int:id>', methods=['GET', 'POST'])
def updateReview(shop, productid, id):
    error = None
    updateReview = CreateReview(request.form)
    if request.method == 'POST':
        review_dict = {}
        try:
            db2 = shelve.open('review.db', 'w')
            review_dict = db2['Review']
        except:
            return redirect(url_for('general_error', errorid=0))
        else:
            try:
                starsgiven = int(updateReview.stars.data)
            except:
                error = 'Please rate with 1 to 5 stars.'
            else:
                review_dict[id].set_stars(starsgiven)
                review_dict[id].set_review(updateReview.review.data)
                file = request.files['photo']
                if file.filename != '':
                    if not allowed_file(file.filename):
                        error = 'The file format must be in jpg, jpeg, png or gif.'
                    else:
                        # Image Handling
                        app.config['UPLOAD_FOLDER'] = './static/uploads/reviews/'
                        filename = secure_filename(file.filename)
                        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        file_extension = os.path.splitext(filename)  # get file type
                        # Make sure to ctrl + f5 to refresh
                        if os.path.exists('static/uploads/reviews/' + str(productid) + file_extension[1]):
                            os.remove('static/uploads/reviews/' + str(productid) + file_extension[1])
                        os.rename('static/uploads/reviews/' + filename,
                                  'static/uploads/reviews/' + str(productid) + file_extension[1])
                        review_dict[id].set_photo(str(productid) + file_extension[1])
                        # End of Image Handling
                db2['Review'] = review_dict
                db2.close()
                return redirect(url_for('viewshopitem', name=shop, productid=productid))
    else:
        ### Check Catalouge id ###
        catalogue_dict = {}
        try:
            db = shelve.open('catalogue.db', 'r')
            catalogue_dict = db['Catalogue']
            db.close()
        except:
            return redirect(url_for('general_error'), errorid=0)

        nomatch = 1
        for key, value in catalogue_dict.items():
            if shop == key:
                for item in catalogue_dict[key]:
                    if item.get_id() == productid:
                        product_name = item.get_name()
                        nomatch = 0
                        break

        if nomatch == 1:
            return redirect(url_for('general_error', errorid=2))
        ##########################
        review_dict = {}
        try:
            db2 = shelve.open('review.db', 'r')
            review_dict = db2['Review']
            db2.close()
        except:
            return redirect(url_for('general_error', errorid=0))

        current_dict = {}
        for item in review_dict:
            if review_dict[item].get_storename() == shop and review_dict[item].get_productid() == productid:
                current_dict[item] = review_dict[item]

        if not current_dict:
            return redirect(url_for('general_error', errorid=3))
        else:
            review = current_dict.get(id)
            updateReview.stars.data = review.get_stars()
            updateReview.review.data = review.get_review()
    return render_template('updateReview.html', form=updateReview, current_dict=current_dict, product_name=product_name, error=error)

#ERROR 404 Not Found Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#ERROR 413: File size is too big
@app.errorhandler(413)
def error413(error):
    return render_template('413.html'), 413

@app.route('/error/<int:errorid>', methods=['GET', 'POST'])
def general_error(errorid):
    title = ""
    message = ""
    if errorid == 0: #Database Error
        title = "Database"
        message = "We were not able to proceed due to a database error. Please try again later."
    elif errorid == 1: #Permission Error
        title = "Permission"
        message = "You do not have sufficient permission to access the information. Please contact our support if you think we made a mistake."
    elif errorid == 2: #Path not accessible Error
        title = "Path Not Accessible"
        message = "You do not have sufficient permission to access the information. Please contact our support if you think we made a mistake."
    elif errorid == 3:
        title = "No review available"
        message = "There is no available reviews for this product."
    else:
        title = "Unknown"
        message = "Something went wrong, please try again later."

    return render_template('error.html', title=title, message=message)



###################################RIDERS START##################################################

@app.route('/riders_home')
def riders_home():
    return render_template('riders_home1.html')


@app.route('/register_complete')
def register_complete():
    return render_template('register_complete.html')


@app.route('/delivery_orders')
def riders_delivery():
    return render_template('delivery_orders.html')


@app.route('/orders_main')
def orders_main():
    return render_template('orders_main.html')


@app.route('/admin_retrieve_riders')
def retrieve_riders():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    riders_list = []
    for key in users_dict:
        user = users_dict.get(key)
        riders_list.append(user)

    return render_template('admin_retrieve_riders.html', count=len(riders_list), riders_list=riders_list)


@app.route('/register_riders', methods=['GET', 'POST'])
def register_riders():
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        users_dict = {}
        user_count_id = 0
        db = shelve.open('storage.db', 'c')
        try:
            users_dict = db['Users']
            user_count_id = int(db['user_count_id'])

        except:
            print("Error in retrieving Users from storage.db.")
        user = Rider.Rider(createUserForm.firstname.data, createUserForm.lastname.data, createUserForm.user_name.data,
                           createUserForm.password.data, createUserForm.email.data, createUserForm.phone_number.data,
                           createUserForm.gender.data, createUserForm.transport.data,
                           createUserForm.license_number.data)
        # auto increment user_id from shelve
        user_count_id = user_count_id + 1
        user.set_user_id(user_count_id)
        db['user_count_id'] = user_count_id

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        db.close()
        return render_template('register_completeRider.html')
    return render_template('register_riders.html', form=createUserForm)


@app.route('/update_riders_admin/<int:id>/', methods=['GET', 'POST'])
def update_rider(id):
    update_user_form = UpdateAdmin(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_user_name(update_user_form.user_name.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)
        user.set_gender(update_user_form.gender.data)
        user.set_transport(update_user_form.transport.data)
        user.set_license_number(update_user_form.license_number.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return redirect(url_for('retrieve_riders'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.user_name.data = user.get_user_name()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()
        update_user_form.gender.data = user.get_gender()
        update_user_form.transport.data = user.get_transport()
        update_user_form.license_number.data = user.get_license_number()

        return render_template('update_riders_admin.html', form=update_user_form)


@app.route('/deleteRider/<int:id>', methods=['POST'])
def delete_rider(id):
    users_dict = {}
    user = users_dict.get(id)
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_firstname() + ' ' + user.get_lastname()
    return redirect(url_for('retrieve_riders'))


@app.route('/login_riders', methods=['GET', 'POST'])
def login_riders():
    error = None
    if request.method == 'POST':
        try:
            users_dict = {}
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print("error")

        if session.get('tailor_account') is not None:
            session.pop('tailor_account')
            session.pop('tailor_identity')
        elif session.get('customer_account') is not None:
            session.pop('customer_account')
            session.pop('customer_identity')
        elif session.get('rider_account') is not None:
            session.pop('rider_account')
            session.pop('rider_identity')

        for user_id in users_dict:
            user = users_dict.get(user_id)
            if request.form['user-name'] == user.get_user_name() and request.form['user-password'] == user.get_password():
                session['rider_account'] = user.get_user_id()
                session['rider_identity'] = user.get_user_name()
                return redirect(url_for('riders_home'))
            elif request.form['user-name'] == 'admin' and request.form['user-password'] == 'admin':
                return redirect(url_for('retrieve_riders'))
            else:
                error = 'Invalid Credentials. Please try again.'

    return render_template('login_riders.html', error=error)

@app.route('/log_out')
def log_out():
    error = None
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    for user_id in users_dict:
        user = users_dict.get(user_id)
        session['rider_account'] = user.get_user_id()
        session['rider_identity'] = user.get_user_name()
    if session['rider_account'] != error:
        session.pop('rider_account')
        session.pop('rider_identity')


    return redirect(url_for('riders_home'))

@app.route('/riders_account', methods=['GET', 'POST'])
def update_riders_details():
    update_user_form = RidersAccounts(request.form)
    user_id = session['rider_account']
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        user = users_dict.get(user_id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)
        user.set_transport(update_user_form.transport.data)
        user.set_license_number(update_user_form.license_number.data)
        user.set_password(update_user_form.password.data)
        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return render_template('riders_account.html', form=update_user_form)

    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(user_id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()
        update_user_form.transport.data = user.get_transport()
        update_user_form.license_number.data = user.get_license_number()
        update_user_form.password.data = user.get_password()

        return render_template('riders_account.html', form=update_user_form)


@app.route('/riders_account/<int:id>/riders_orders')
def riders_orders(id):
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']

    user = users_dict.get(id)
    db.close()

    session['user_updated'] = user.get_firstname() + ' ' + user.get_lastname()
    return render_template('riders_orders.html')

#################################RIDERS END#################################################

##################################TAILORS START#############################################
@app.route('/tailors_home')
def tailors_home():
    return render_template('tailors_home.html')


@app.route('/register_tailors', methods=['GET', 'POST'])
def register_tailors():
    createUserForm = RegisterTailors(request.form)
    if request.method == 'POST' and createUserForm.validate():
        tailor_dict = {}
        tailor_count_id = 0
        db = shelve.open('tailor_storage.db', 'c')
        try:
            tailor_dict = db['Tailors']
            tailor_count_id = int(db['tailor_count_id'])

        except:
            print("Error in retrieving Users from storage.db.")
        # print(createUserForm.firstname.data)
        user = Tailor.Tailor(createUserForm.firstname.data, createUserForm.lastname.data, createUserForm.user_name.data, createUserForm.password.data, createUserForm.store_name.data, createUserForm.address1.data, createUserForm.address2.data, createUserForm.city.data, createUserForm.postal_code.data,createUserForm.email.data, createUserForm.phone_number.data)
        # auto increment user_id from shelve
        tailor_count_id = tailor_count_id + 1
        user.set_user_id(tailor_count_id)
        db['tailor_count_id'] = tailor_count_id

        tailor_dict[user.get_user_id()] = user
        db['Tailors'] = tailor_dict
        db.close()
        return render_template('register_completeTailor.html')

    return render_template('register_tailors.html', form=createUserForm)


@app.route('/admin_retrieve_tailors')
def retrieve_tailors():
    tailor_dict = {}
    db = shelve.open('tailor_storage.db', 'r')
    tailor_dict = db['Tailors']
    db.close()

    tailor_list = []
    for key in tailor_dict:
        tailor = tailor_dict.get(key)
        tailor_list.append(tailor)

    return render_template('admin_retrieve_tailors.html', count=len(tailor_list), tailor_list=tailor_list)


@app.route('/update_tailors_admin/<int:id>/', methods=['GET', 'POST'])
def update_tailor(id):
    update_user_form = AdminUpdateTailor(request.form)
    if request.method == 'POST' and update_user_form.validate():
        tailor_dict = {}
        db = shelve.open('tailor_storage.db', 'w')
        tailor_dict = db['Tailors']

        user = tailor_dict.get(id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_user_name(update_user_form.user_name.data)
        user.set_store_name(update_user_form.store_name.data)
        user.set_address1(update_user_form.address1.data)
        user.set_address2(update_user_form.address2.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_city(update_user_form.city.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)

        db['Tailors'] = tailor_dict
        db.close()

        session['user_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return redirect(url_for('retrieve_tailors'))
    else:
        tailor_dict = {}
        db = shelve.open('tailor_storage.db', 'r')
        tailor_dict = db['Tailors']
        db.close()

        user = tailor_dict.get(id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.user_name.data = user.get_user_name()
        update_user_form.store_name.data = user.get_store_name()
        update_user_form.address1.data = user.get_address1()
        update_user_form.address2.data = user.get_address2()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.city.data = user.get_city()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()

        return render_template('update_tailors_admin.html', form=update_user_form)


@app.route('/deleteTailor/<int:id>', methods=['POST'])
def delete_tailor(id):
    tailor_dict = {}
    user = tailor_dict.get(id)
    db = shelve.open('tailor_storage.db', 'w')
    tailor_dict = db['Tailors']

    user = tailor_dict.pop(id)

    db['Tailors'] = tailor_dict
    db.close()

    session['user_deleted'] = user.get_firstname() + ' ' + user.get_lastname()
    return redirect(url_for('retrieve_tailors'))


@app.route('/login_tailors', methods=['GET', 'POST'])
def tailors_login():
    error = None
    if request.method == 'POST':
        try:
            tailor_dict = {}
            db = shelve.open('tailor_storage.db', 'r')
            tailor_dict = db['Tailors']
            db.close()
        except:
            print("error")

        if session.get('tailor_account') is not None:
            session.pop('tailor_account')
            session.pop('tailor_identity')
        elif session.get('customer_account') is not None:
            session.pop('customer_account')
            session.pop('customer_identity')
        elif session.get('rider_account') is not None:
            session.pop('rider_account')
            session.pop('rider_identity')

        for user_id in tailor_dict:
            user = tailor_dict.get(user_id)
            if request.form['user-name'] == user.get_user_name() and request.form['user-password'] == user.get_password():
                session['tailor_account'] = user.get_user_id()
                session['tailor_identity'] = user.get_user_name()
                return redirect(url_for('tailors_home'))
            # Do this for the rest of the admins
            elif (request.form['user-name'] == 'Admin') and request.form['user-password'] == tailor_dict.get(3).get_password():
                session['tailor_account'] = 3
                session['tailor_identity'] = 'Admin'
                return redirect(url_for('retrieve_tailors'))
            else:
                error = 'Invalid Credentials. Please try again.'


    return render_template('login_tailors.html', error=error)


@app.route('/log_out_tailors')
def log_out_tailors():
    error = None
    db = shelve.open('tailor_storage.db', 'r')
    tailor_dict = db['Tailors']
    for user_id in tailor_dict:
        user = tailor_dict.get(user_id)
        session['tailor_account'] = user.get_user_id()
        session['tailor_identity'] = user.get_user_name()
    if session['tailor_account'] != error:
        session.pop('tailor_account')
        session.pop('tailor_identity')
    if session.get('tailor_account') is not None:
        session.pop('tailor_account')
        session.pop('tailor_identity')

    db.close()

    return redirect(url_for('tailors_home'))


@app.route('/tailors_account', methods=['GET', 'POST'])
def update_tailors_details():
    update_user_form = TailorsAccount(request.form)
    user_id = session['tailor_account']
    if request.method == 'POST' and update_user_form.validate():
        tailor_dict = {}
        db = shelve.open('tailor_storage.db', 'w')
        tailor_dict = db['Tailors']
        user = tailor_dict.get(user_id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_store_name(update_user_form.store_name.data)
        user.set_address1(update_user_form.address1.data)
        user.set_address2(update_user_form.address2.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_city(update_user_form.city.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)
        user.set_password(update_user_form.password.data)
        db['Tailors'] = tailor_dict
        db.close()

        session['user_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return render_template('tailors_account.html', form=update_user_form)

    else:
        tailor_dict = {}
        db = shelve.open('tailor_storage.db', 'r')
        tailor_dict = db['Tailors']
        db.close()

        user = tailor_dict.get(user_id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.store_name.data = user.get_store_name()
        update_user_form.address1.data = user.get_address1()
        update_user_form.address2.data = user.get_address2()
        update_user_form.city.data = user.get_city()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()
        update_user_form.password.data = user.get_password()

        return render_template('tailors_account.html', form=update_user_form)

##################################TAILORS END#############################################

@app.route('/register_customers', methods=['GET', 'POST'])
def register_customers():
    createUserForm = Customer_Register(request.form)
    if request.method == 'POST' and createUserForm.validate():
        customer_dict = {}
        user_count_id = 0
        db = shelve.open('customer.db', 'c')
        try:
            customer_dict = db['Customer']
            user_count_id = int(db['user_count_id'])

        except:
            print("Error in retrieving Users from storage.db.")
        user = Customer.Customer(createUserForm.firstname.data, createUserForm.lastname.data, createUserForm.user_name.data,
                           createUserForm.password.data, createUserForm.address1.data, createUserForm.address2.data, createUserForm.city.data, createUserForm.postal_code.data,
                           createUserForm.gender.data, createUserForm.email.data,
                           createUserForm.phone_number.data)
        # auto increment user_id from shelve
        user_count_id = user_count_id + 1
        user.set_user_id(user_count_id)
        db['user_count_id'] = user_count_id

        customer_dict[user.get_user_id()] = user
        db['Customer'] = customer_dict
        db.close()
        return render_template('register_completeCustomer.html')
    return render_template('CustRegister.html', form=createUserForm)


@app.route('/admin_retrieve_customers')
def retrieve_customers():
    customer_dict = {}
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()

    customers_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        customers_list.append(customer)

    return render_template('admin_retrieve_customers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/update_customer_admin/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_user_form = Customer_AdminUpdate(request.form)
    if request.method == 'POST' and update_user_form.validate():
        customer_dict = {}
        db = shelve.open('customer.db', 'w')
        customer_dict = db['Customer']

        user = customer_dict.get(id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_user_name(update_user_form.user_name.data)
        user.set_address1(update_user_form.address1.data)
        user.set_address2(update_user_form.address2.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_city(update_user_form.city.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)

        db['Customer'] = customer_dict
        db.close()

        session['customer_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return redirect(url_for('retrieve_customers'))
    else:
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()

        user = customer_dict.get(id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.user_name.data = user.get_user_name()
        update_user_form.address1.data = user.get_address1()
        update_user_form.address2.data = user.get_address2()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.city.data = user.get_city()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()

        return render_template('update_customer_admin.html', form=update_user_form)


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_dict = {}
    user = customer_dict.get(id)
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customer']

    user = customer_dict.pop(id)

    db['Customer'] = customer_dict
    db.close()

    session['customer_deleted'] = user.get_firstname() + ' ' + user.get_lastname()
    return redirect(url_for('retrieve_customers'))


@app.route('/login_customers', methods=['GET', 'POST'])
def login_customers():
    error = None
    if request.method == 'POST':
        try:
            customer_dict = {}
            db = shelve.open('customer.db', 'r')
            customer_dict = db['Customer']
        except:
            print("error")

        if session.get('tailor_account') is not None:
            session.pop('tailor_account')
            session.pop('tailor_identity')
        elif session.get('customer_account') is not None:
            session.pop('customer_account')
            session.pop('customer_identity')
        elif session.get('rider_account') is not None:
            session.pop('rider_account')
            session.pop('rider_identity')

        for user_id in customer_dict:
            user = customer_dict.get(user_id)
            if request.form['user-name'] == user.get_user_name() and request.form['user-password'] == user.get_password():
                session['customer_account'] = user.get_user_id()
                session['customer_identity'] = user.get_user_name()
                return redirect(url_for('home_page'))
            elif request.form['user-name'] == 'customer_admin' and request.form['user-password'] == 'customer_admin':
                return redirect(url_for('retrieve_customers'))
            else:
                error = 'Invalid Credentials. Please try again.'

    return render_template('login_customers.html', error=error)


@app.route('/customers_account', methods=['GET', 'POST'])
def update_customers_details():
    update_user_form = Customer_Update(request.form)
    user_id = session['customer_account']
    if request.method == 'POST' and update_user_form.validate():
        customer_dict = {}
        db = shelve.open('customer.db', 'w')
        customer_dict = db['Customer']
        user = customer_dict.get(user_id)
        user.set_firstname(update_user_form.firstname.data)
        user.set_lastname(update_user_form.lastname.data)
        user.set_address1(update_user_form.address1.data)
        user.set_address2(update_user_form.address2.data)
        user.set_city(update_user_form.city.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)
        user.set_password(update_user_form.password.data)
        db['Customer'] = customer_dict
        db.close()

        session['customer_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return render_template('customer_account.html', form=update_user_form)

    else:
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()

        user = customer_dict.get(user_id)
        update_user_form.firstname.data = user.get_firstname()
        update_user_form.lastname.data = user.get_lastname()
        update_user_form.address1.data = user.get_address1()
        update_user_form.address2.data = user.get_address2()
        update_user_form.city.data = user.get_city()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()
        update_user_form.password.data = user.get_password()

        return render_template('customer_account.html', form=update_user_form)


@app.route('/log_out_customers')
def log_out_customers():
    error = None
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    for user_id in customer_dict:
        user = customer_dict.get(user_id)
        session['customer_account'] = user.get_user_id()
        session['customer_identity'] = user.get_user_name()
    if session['customer_account'] != error:
        session.pop('customer_account')
        session.pop('customer_identity')
    if session.get('customer_account') is not None:
        session.pop('customer_account')
        session.pop('customer_identity')

    return redirect(url_for('home'))

########################################## Start of Stacey's code ##########################################
@app.route('/CreateCourse', methods=['GET', 'POST'])
def CreateCourse():
    error = None
    if session['tailor_account'] != "":
        createcourse = CreateCourseForm(request.form)


        if request.method == 'POST' and createcourse.validate():
            tailor_storename = "Admin Store Lah"
            if session['tailor_identity'] != "Admin":
                tailor_storename = get_userdata("tailor").get_store_name()
            #tailor_dict = {}
            courseDict = {}
            courseid_count = 0
            try:
                db = shelve.open('course.db', 'c')
                courseDict = db['course']
                courseid_count = int(db['courseid_count']) #
            except:
                print("error reading course.db")


            if 'image' not in request.files:
                error = 'Something went wrong, please refresh page.'

            file = request.files[createcourse.tbnail.name]
            print(file.filename)
            if file.filename == '':
                error = 'Please upload a file.'
            else:
                app.config['UPLOAD_FOLDER'] = './static/uploads/courseban/'

                filename = secure_filename(file.filename)
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if not allowed_course_file(file.filename):
                    error = 'The file format must be in jpg, jpeg, png or gif.'

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_extension = os.path.splitext(filename)  # get file type
                os.rename('static/uploads/courseban/' + filename, 'static/uploads/courseban/' + str(courseid_count) + file_extension[1])

                #if error is None:
                course = Course.Course(createcourse.title.data, tailor_storename, createcourse.material.data,
                                   createcourse.language.data, createcourse.livecourse.data,createcourse.note.data,
                                   createcourse.price.data, 'static/uploads/courseban/' + str(courseid_count) + file_extension[1])

                courseid_count = courseid_count + 1
                course.set_courseid(courseid_count)
                db["courseid_count"] = courseid_count

                courseDict[course.get_courseid()] = course
                db["course"] = courseDict
                db.close()


                return redirect(url_for('viewcourse', error=error))  #??? what

    return render_template('CreateCourse.html', form=createcourse, error=error)


@app.route('/ViewCourse')
def viewcourse():
    if session['tailor_account'] != "":
        courseDict = {}
        try:
            db = shelve.open('course.db', 'r')  # open shelve
            courseDict = db['course']  # retrieve users
            db.close()
        except:
            print("Error retrieving users from course.db")

        tailor_storename = "Admin Store Lah"
        if session['tailor_identity'] != "Admin":
            tailor_storename = get_userdata("tailor").get_store_name()

        courseList = []
        for key,value in courseDict.items():
            print(value.get_tailor())
            if value.get_tailor() == tailor_storename:
                course = courseDict.get(key)  # key is user id
                courseList.append(course)

    return render_template('ViewCourse.html', count=len(courseList), courseList=courseList)  # red is like parameters
    # parse in 2 variables, count and users_list



@app.route('/UpdateCourse/<int:id>', methods=['GET','POST'])  #??????????????
def UpdateCourse(id):
    updatecourse = CreateCourseForm(request.form)
    if request.method == 'POST' and updatecourse.validate(): #???

        tailor_storename = "Admin Store Lah"
        if session['tailor_identity'] != "Admin":
            tailor_storename = get_userdata("tailor").get_store_name()

        courseDict = {}
        db = shelve.open('course.db', 'w')
        courseDict = db['course']

        course = courseDict.get(id)  # id?
        course.set_title(updatecourse.title.data)
        #course.set_tailor(updatecourse.tailor.data)
        course.set_material(updatecourse.material.data)
        course.set_language(updatecourse.language.data)
        course.set_livecourse(updatecourse.livecourse.data)
        course.set_note(updatecourse.note.data)
        course.set_price(updatecourse.price.data)

        db['course'] = courseDict
        db.close()

        session['course_updated'] = course.get_title()

        #change to saved notif
        return redirect(url_for('viewcourse'))

    else:
        courseDict = {}
        db = shelve.open('course.db', 'r')
        courseDict = db['course']

        db.close()

        course = courseDict.get(id)  # ??
        updatecourse.title.data = course.get_title()
        #updatecourse.tailor.data = course.get_tailor()
        updatecourse.material.data = course.get_material()
        updatecourse.language.data = course.get_language()
        updatecourse.livecourse.data = course.get_livecourse()
        updatecourse.note.data = course.get_note()
        updatecourse.price.data = course.get_price()
        updatecourse.tbnail.data = course.get_tbnail()

        return render_template('UpdateCourse.html', form=updatecourse, course=course)



@app.route('/DeleteCourse/<int:id>', methods=['POST']) #?????????????
def DeleteCourse(id):
    courseDict = {}
    db = shelve.open('course.db', 'w')
    courseDict = db['course']

    courseDict.pop(id)

    db['course'] = courseDict
    db.close()

    return redirect(url_for('viewcourse'))



# View all courses avaliable
@app.route('/ViewShopsCourse')
def viewshopscourse():
    courseDict = {}
    try:
        db = shelve.open('course.db', 'r')  # open shelve
        courseDict = db['course']  # retrieve users
        db.close()
    except:
        print("Error retrieving users from course.db")

    print(courseDict)


    return render_template('ViewShopsCourse.html', courseDict=courseDict)


# View individual course info
@app.route('/course/<int:id>', methods=['GET','POST']) #/<int:id>
def indivCourse(id):
    customer_dict = {}
    courseDict = {}
    keyid_count = 0
    try:
        db = shelve.open('course.db', 'r')  # open shelve
        courseDict = db['course'] # retrieve users

        db.close()
    except:
        print("Error retrieving from course.db")

    courseInfo = courseDict.get(id)
    #customerid = session['customer_account']
    #custID = courseInfo.set_customerid(customerid)

    if request.method=="POST":
        req = request.form
        timeslot = req.get("timeslot")  #put timeslot into cart??
        #title, tailor, price, courseid
        cart = Cart.Cart(courseInfo.get_title(), courseInfo.get_tailor(), courseInfo.get_price(),
                         id, session['customer_account'] )

        #keyid_count = keyid_count + 1
        #
        #cart.set_keyid(keyid_count)
        #
        courseCart[id] = cart


        return redirect(url_for('coursepayment'))


    return render_template('course.html',  courseInfo=courseInfo) ##idk


@app.route('/CoursePayment')
def coursepayment():
    #print("here2:" , courseCart)
    #print(session['customer_account'] )

    total = 0
    for course in courseCart:
        total += courseCart[course].get_price()

    print(total)

    return render_template('CoursePayment.html',  courseCart=courseCart, total=total)

@app.route('/CoursePaymentSuccess')
def coursetransactionsuccess():
    print("here3:", courseCart)
    try:
        db = shelve.open('signedcourse.db', 'c')
        db['signedcourse'] = courseCart
        #print(courseCart , "here")
    except:
        print("Error retrieving from signedcourse.db")

    #courseCart[] = signedcourse
    #db["signedcourse"] = courseCart
    db.close()

    return render_template('CoursePaymentSuccessful.html')

@app.route('/DeleteCourseCart/<int:id>')  # ?????????????lollolololol
def deletecoursecart(id):
    courseDict = {}
    try:
        db = shelve.open('course.db', 'r')  # open shelve
        courseDict = db['course']  # retrieve users
        db.close()
    except:
        print("Error retrieving users from course.db")

    courseInfo = courseDict.get(id)

    # print(courseCart)
    cart = Cart.Cart(courseInfo.get_title(), courseInfo.get_tailor(), courseInfo.get_price(),
                     id, session['customer_account'] )
    courseCart[id] = cart

    courseCart.pop(id)

    return redirect(url_for('coursepayment', courseCart=courseCart))



@app.route('/AddContent/<int:id>', methods=['GET', 'POST'])
def AddContent(id):
    contentDict = {}
    courseDict = {}
    error = None
    addcontent = AddContentForm(request.form)
    try:
        db = shelve.open('content.db', 'r')
        contentDict = db['content']
        # videoid_count = int(db['videoid_count']) #
        db.close()
    except:
        print("error reading content.db")

    course = courseDict.get(id)
    contentList = []
    for key in contentDict:
        content = contentDict.get(key)  # key is topic
        contentList.append(content)

    addcontent = AddContentForm(request.form)
    #print(addcontent.validate())
    if request.method == 'POST' and addcontent.validate():

        contentDict = {}
        courseDict = {}
        #videoid_count = 0
        try:
           db = shelve.open('content.db', 'c')
           contentDict = db['content']
           #videoid_count = int(db['videoid_count']) #
        except:
           print("error reading content.db")

        course = courseDict.get(id)

        if 'video' not in request.files:
            error = 'Something went wrong, please refresh page.'

        vidfile = request.files[addcontent.video.name]
        #print(vidfile.filename)
        if vidfile.filename == '':
            error = 'Please upload a file.'
        else:
            app.config['UPLOAD_FOLDER'] = './static/uploads/coursevideo/' + str(id)
            if not os.path.exists('./static/uploads/coursevideo/' + str(id)): #??
                os.makedirs('./static/uploads/coursevideo/' + str(id))
            if not allowed_course_file(vidfile.filename):
                error = 'The file format must be in .mp4 or .mov .'

            filename = secure_filename(vidfile.filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
               os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            vidfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if error is None:
                content = Content.Content(addcontent.topic.data, filename, id)

                db[addcontent.topic.data] = content
                contentDict[content.get_topic()] = content
                db['content'] = contentDict
                db.close()

                return redirect(url_for('AddContent', id=id, error=error))  #??? what

    return render_template('AddContent.html',form=addcontent, count=len(contentList), contentList=contentList, id=id, error=error)

@app.route('/DeleteContent/<int:id>/<topic>', methods=['GET', 'POST']) #?????????????lollolololol
def DeleteContent(id, topic):
    contentDict = {}

    db = shelve.open('content.db', 'w')
    contentDict = db['content']

    #print(contentDict)
    if id == contentDict[topic].get_course():
        contentDict.pop(topic)

    db['content'] = contentDict
    db.close()

    return redirect(url_for('AddContent', id=id, topic=topic))



@app.route('/EdPlatform')
def edplatform():
    courseDict = {}
    contentDict = {}
    #print("this here:" )
    try:
        db1 = shelve.open('signedcourse.db', 'r')  # open shelve
        courseCart = db1['signedcourse']  # retrieve users

        db = shelve.open('course.db', 'r')  # open shelve
        courseDict = db['course']  # retrieve users

    except:
        print("Error retrieving from course.db")

    customer_courses = {} #To pass this this dict to html
    for key,value in courseCart.items():
        if session['customer_account'] == value.get_customerid():
            customer_courses[key] = value
        # print(value.get_courseid())

    print(customer_courses)
        #print(db['signedcourse'])

    db1.close()
    db.close()


    return render_template('EdPlatform.html', customer_courses=customer_courses, courseDict=courseDict) #, courseDict=courseDict, count=len(courseList), #courseList=courseList, signedcourseList=signedcourseList, courseCart=courseCart )


@app.route('/EdPlatCourseContent/<int:id>/<topic>')
def EdPlatCourseContent(id, topic):
    contentDict = {}
    courseDict = {}

    print("print this",id)

    try:
        db = shelve.open('content.db', 'r')  # open shelve
        contentDict = db['content']  # retrieve users
        db.close()
        # print("print", contentDict.get(topic).get_video())

        db2 = shelve.open('course.db', 'r')  # open shelve
        courseDict = db2['course']  # retrieve users
        db2.close()
    except:
        print("Error opening db")

    actualContent = {}
    for key, value in contentDict.items():
        if id == value.get_course():
            actualContent[key] = value
            print(value.get_video())
            print(actualContent)
    # print(contentDict[t].get_topic())

    return render_template('EdPlatCourseContent.html' ,id=str(id), contentDict=actualContent, courseDict=courseDict, topic=topic)


######################################## End of Stacey's code #####################################

######################################## Start of Kai Jie's code #####################################
@app.route('/createOrder', methods=['GET', 'POST'])
def create_Order():
    createcOrder = createOrder(request.form)

    if request.method == 'POST' and createcOrder.validate():
        ordersDict = {}
        order_count_id = 0
        db = shelve.open('orders.db', 'c')
        try:
            ordersDict = db['orders']
            order_count_id = int(db['order_count_id'])
        except:
            print("error reading orders.db")

        custOrder = Orders.Orders(createcOrder.cname.data, createcOrder.description.data,
                                  createcOrder.price.data, createcOrder.due_date.data, )

        order_count_id = order_count_id + 1
        custOrder.set_order_id(order_count_id)
        db['order_count_id'] = order_count_id
        ordersDict[custOrder.get_order_id()] = custOrder
        db['orders'] = ordersDict
        db.close()
        return redirect(url_for('thankyou'))

    return render_template('createOrders.html', form=createcOrder)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/vieworders')
def vieworders():
    transaction_dict = {}
    try:
        db = shelve.open('transaction_orders', 'r')
        transaction_dict = db['Transaction_Orders']
    except:
        print("error!")

    #for i in order_list:
        #print (i.get_order_id())

    return render_template('vieworders.html', transaction_orders=transaction_dict)

@app.route('/completedOrders/<int:id>', methods=['POST'])
def completedOrders(id):
    ordersDict = {}
    db = shelve.open('orders.db', 'w')
    ordersDict = db['orders']

    ordersDict.pop(id)

    db['orders'] = ordersDict
    db.close()

    return redirect(url_for('vieworders'))

@app.route('/salesChart', methods=['GET', 'POST'])
def salesChart():
    targetDict = {}
    try:
        db = shelve.open('target.db', 'r')
        targetDict = db['target']
        db.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    tailor_storename = "Admin Store Lah"
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    print(targetDict)
    target_list = []
    print(tailor_storename)
    for key,value in targetDict.items():
        print(value.get_store_name())
        if value.get_store_name() == tailor_storename:
            ttarget = targetDict.get(key)
            target_list.append(ttarget)
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = ['1165', '1135']
    updatetarget = updateTarget(request.form)
    if request.method == 'POST' and updatetarget.validate():
        return redirect(url_for('targetSales'))
    return render_template('salesChart.html', labels=labels, data=data, target_list=target_list)

@app.route('/targetSales', methods=['GET', 'POST'])
def targetSales():
    updatetarget = updateTarget(request.form)
    tailor_storename = "Admin Store Lah"
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    if request.method == 'POST' and updatetarget.validate():
        targetDict = {}
        try:
            db = shelve.open('target.db', 'w')
            targetDict = db['target']
        except:
            print("db error")

        try:
            count_id = max(targetDict, key=int) + 1
        except:
            count_id = 1

        check_count = 0
        if len(targetDict) >0:
            for key,value in targetDict.items():
                if value.get_store_name() == tailor_storename:
                    value.set_target(updatetarget.target.data)
                    check_count += 1
            db['target'] = targetDict
            db.close()

        print(check_count)
        if check_count == 0:
            try:
                db = shelve.open('target.db', 'c')
                targetDict = db['target']
            except:
                print("db error")

            ttarget = Target.Target(updatetarget.target.data, tailor_storename)
            targetDict[count_id] = ttarget
            db['target'] = targetDict
            db.close()

        return redirect(url_for('salesChart'))


    return render_template('targetSales.html', form=updatetarget)

@app.route('/custChart', methods=['GET', 'POST'])
def custChart():
    availDict = {}
    try:
        db = shelve.open('avail.db', 'r')
        availDict = db['avail']
        db.close()
    except:
        return redirect(url_for('general_error', errorid=0))

    tailor_storename = "Admin Store Lah"
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    print(availDict)
    avail_list = []
    for key, value in availDict.items():
        print(value.get_store_name())
        if value.get_store_name() == tailor_storename:
            avail = availDict.get(key)
            avail_list.append(avail)

    labels = ['week 1', 'week 2', 'week 3', 'week 4']
    updateavail = updateAvail(request.form)
    if request.method == 'POST' and updateavail.validate():
        return redirect(url_for('availability'))
    return render_template('custChart.html', labels=labels, avail_list=avail_list)

@app.route('/availability', methods=['GET', 'POST'])
def availability():
    updateavail = updateAvail(request.form)
    tailor_storename = "Admin Store Lah"
    if session['tailor_identity'] != "Admin":
        tailor_storename = get_userdata("tailor").get_store_name()

    if request.method == 'POST' and updateavail.validate():
        availDict = {}
        try:
            db = shelve.open('avail.db', 'w')
            availDict = db['avail']
        except:
            print("db error")

        try:
            count_id = max(availDict, key=int) + 1
        except:
            count_id = 1

        check_count = 0
        if len(availDict) >0:
            for key,value in availDict.items():
                if value.get_store_name() == tailor_storename:
                    value.set_availstart(updateavail.availstart.data)
                    value.set_availend(updateavail.availend.data)
                    check_count += 1
            db['avail'] = availDict
            db.close()

        print(check_count)
        if check_count == 0:
            try:
                db = shelve.open('avail.db', 'c')
                availDict = db['avail']
            except:
                print("db error")

            avail = Availability.Availability(updateavail.availstart.data, updateavail.availend.data, tailor_storename)
            availDict[count_id] = avail
            db['avail'] = availDict
            db.close()

        return redirect(url_for('custChart'))

    return render_template('availability.html', form=updateavail)

@app.route('/addVoucher', methods=['GET', 'POST'])
def add_voucher():
    AddVoucher = addVoucher(request.form)

    if request.method == 'POST' and AddVoucher.validate():
        voucherDict = {}
        voucher_count_id = 0
        db = shelve.open('vouchers.db', 'c')
        try:
            voucherDict = db['vouchers']
            voucher_count_id = int(db['voucher_count_id'])
        except:
            print("error reading voucher.db")

        voucher = Vouchers.Vouchers(AddVoucher.code.data, AddVoucher.description.data, AddVoucher.discount.data, AddVoucher.minpurchase.data,
                                    AddVoucher.quantity.data, AddVoucher.vstartdate.data, AddVoucher.vexpirydate.data,)

        voucher_count_id = voucher_count_id + 1
        voucher.set_voucher_id(voucher_count_id)
        db['voucher_count_id'] = voucher_count_id
        voucherDict[voucher.get_voucher_id()] = voucher
        db['vouchers'] = voucherDict
        db.close()
        return redirect(url_for('voucherList'))

    return render_template('addVouchers.html', form=AddVoucher)

@app.route('/voucherList')
def voucherList():
    voucherDict = {}
    try:
        db = shelve.open('vouchers.db', 'r')
        voucherDict = db['vouchers']
        db.close()
    except:
        return redirect(url_for('dberror'))

    voucher_list = []
    for key in voucherDict:
        voucher = voucherDict.get(key)
        voucher_list.append(voucher)

    return render_template('voucherList.html',count=len(voucher_list), voucher_list=voucher_list)

@app.route('/updateVoucher/<int:id>/', methods=['GET', 'POST'])
def update_voucher(id):
    UpdateVoucher = addVoucher(request.form)
    if request.method == 'POST' and UpdateVoucher.validate():
        voucherDict = {}
        db = shelve.open('vouchers.db', 'w')
        voucherDict = db['vouchers']

        voucher = voucherDict.get(id)
        voucher.set_code(UpdateVoucher.code.data)
        voucher.set_description(UpdateVoucher.description.data)
        voucher.set_discount(UpdateVoucher.discount.data)
        voucher.set_minpurchase(UpdateVoucher.minpurchase.data)
        voucher.set_quantity(UpdateVoucher.quantity.data)
        voucher.set_vstartdate(UpdateVoucher.vstartdate.data)
        voucher.set_vexpirydate(UpdateVoucher.vexpirydate.data)

        db['vouchers'] = voucherDict
        db.close()

        return redirect(url_for('voucherList'))
    else:
        voucherDict = {}
        db = shelve.open('vouchers.db', 'r')
        voucherDict = db['vouchers']
        db.close()

        voucher = voucherDict.get(id)
        UpdateVoucher.code.data = voucher.get_code()
        UpdateVoucher.description.data = voucher.get_description()
        UpdateVoucher.discount.data = voucher.get_discount()
        UpdateVoucher.minpurchase.data = voucher.get_minpurchase()
        UpdateVoucher.quantity.data = voucher.get_quantity()
        UpdateVoucher.vstartdate.data = voucher.get_vstartdate()
        UpdateVoucher.vexpirydate.data = voucher.get_vexpirydate()

        return render_template('updateVouchers.html', form=UpdateVoucher)

@app.route('/deleteVoucher/<int:id>', methods=['POST'])
def deleteVoucher(id):
    voucherDict = {}
    db = shelve.open('vouchers.db', 'w')
    voucherDict = db['vouchers']

    voucherDict.pop(id)

    db['vouchers'] = voucherDict
    db.close()

    return redirect(url_for('voucherList'))
######################################## End of Kai Jie's code #####################################
@app.route('/my_orders')
def customer_orders():
    transaction_dict = {}
    try:
        db = shelve.open('transaction_orders', 'r')
        transaction_dict = db['Transaction_Orders']
    except:
        print("error!")

    for key, value in transaction_dict.items():
        print(value[0]) #Example Get store name

    return render_template('customer_orders.html', transaction_orders=transaction_dict)


@app.route('/transaction_complete')
def transaction_complete():
    #Retrieve Example
    try:
        transaction_dict = {}
        db = shelve.open('transaction_orders', 'r')
        transaction_dict = db['Transaction_Orders']
    except:
        print("error!")

    # for key, value in transaction_dict.items():
    #     print(value[0]) #Example Get store name

    return render_template('transaction_complete.html')


@app.route('/customers_checkout', methods=['GET', 'POST'])
def customers_checkout():
    # user_id = session['customer_account']
    # if user_id is not None:


    # Issue 3 - if session cart is empty, must redirect them, if not they will see the attribute error.
    if session.get('cart_session') is None:
        return redirect(url_for('general_error', errorid=4))
    else:
        # Here you go for your total.
        total = 0
        for key, value in session["cart_session"].items():
            total += value[4] * value[3]
            print(session['cart_session'])
    # customer_checkout = Customer_Checkout(request.form)
    # user_id = session['customer_account']
    delivery_details = Deliver_Options(request.form)
    user_id = session['customer_account']
    if request.method == 'POST' and delivery_details.validate():
        customer_dict = {}
        transaction_dict = {}
        db = shelve.open('customer.db', 'w')
        customer_dict = db['Customer']
        try:
            db = shelve.open('transaction_orders', 'c')
            transaction_dict = db['Transaction_Orders']
        except:
            print("error!")

        for key, value in session["cart_session"].items():
            value.append(delivery_details.firstname.data + ' ' + delivery_details.lastname.data)
            value.append(delivery_details.address1.data + ' ' + delivery_details.address2.data +',' + delivery_details.city.data + '' + delivery_details.postal_code.data)
            value.append(delivery_details.email.data)
            value.append(delivery_details.phone_number.data)
            value.append(delivery_details.order_notes.data)
            value.append(delivery_details.delivery_options.data)
            value.append(delivery_details.delivery_time.data)
            value.append(delivery_details.delivery_date.data)
        # Issue 5 your old script doesnt rename the key, so if the same keys are written into the db, they will be overwritten.
        # This part will resolve the replicated key issue
        for key, value in session["cart_session"].items():
            try:
                count_id = max(transaction_dict, key=int) + 1
            except:
                count_id = 1
            transaction_dict[count_id] = value

        # Issue 4, don't need to set your customer details, you not updating your customer db.
        # user = customer_dict.get(user_id)
        # user.set_firstname(customer_checkout.firstname.data)
        # user.set_lastname(customer_checkout.lastname.data)
        # user.set_address1(customer_checkout.address1.data)
        # user.set_address2(customer_checkout.address2.data)
        # user.set_postal_code(customer_checkout.postal_code.data)
        # user.set_city(customer_checkout.city.data)
        # user.set_email(customer_checkout.email.data)
        # user.set_phone_number(customer_checkout.phone_number.data)

        db['Transaction_Orders'] = transaction_dict
        print("db", db['Transaction_Orders'])
        db.close()

        session.pop('cart_session', None)
        session.pop('cart_id', None)
        return redirect(url_for('transaction_complete'))
        # Issue 2 return render_template('customer_checkout.html', form=customer_checkout)
    else:
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()

        user = customer_dict.get(user_id)
        delivery_details.firstname.data = user.get_firstname()
        delivery_details.lastname.data = user.get_lastname()
        delivery_details.address1.data = user.get_address1()
        delivery_details.address2.data = user.get_address2()
        delivery_details.postal_code.data = user.get_postal_code()
        delivery_details.city.data = user.get_city()
        delivery_details.email.data = user.get_email()
        delivery_details.phone_number.data = user.get_phone_number()
        return render_template('customer_checkout.html', form=delivery_details, total=total)

    # else:
    #     return render_template('404.html')


@app.route('/deleteCartItem/<id>', methods=['GET', 'POST'])
def delete_cartitem(id):
    cart_dict = session.get("cart_session")
    cart_dict.pop(id)
    session["cart_session"] = cart_dict
    session["cart_id"] -= 1
    return redirect(url_for('customers_checkout'))


@app.route('/order_listings')
def riders_listings():
    transaction_dict = {}
    try:
        db = shelve.open('transaction_orders', 'r')
        transaction_dict = db['Transaction_Orders']
    except:
        print("error!")

    for key, value in transaction_dict.items():
        print(value[0]) #Example Get store name

    return render_template('Riders_Orders_Listings.html', transaction_orders=transaction_dict)



if __name__ == '__main__':
    app.debug = True
    app.run()
