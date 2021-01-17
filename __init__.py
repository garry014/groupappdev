from flask import Flask, render_template, request, redirect, url_for, Request, session
from Forms import *
from cregform import *
import os, pathlib, shelve, Ads, CustRegister, Catalogue, Chat, Notification
from datetime import datetime as dt
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

from Admin_Update_Form import UpdateAdmin
from Register_Form import CreateUserForm
from Forms_Riders import RidersAccounts
import Rider

username = "Admin"  #Test Scriptdas

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #File upload size cap 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            if values.get_recipient() == username:
                my_noti[key] = values
                if values.get_status() == "new":
                    count += 1
                    print(count)

        rev_dict = {}
        for i in sorted(my_noti.keys(), reverse=True):
            rev_dict[i] = my_noti[i]
        return rev_dict, count

app.jinja_env.globals.update(view_notification=view_notification)


def create_notification(recipient, category, message, hyperlink):
    #noti = notification
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
        if action == "readall":
            for noti in noti_dict:
                if username == noti_dict[noti].get_recipient():
                    noti_dict[noti].set_status("read")
        elif action == "delete":
            if username == noti_dict[id].get_recipient():
                noti_dict.pop(id)

        db1['Notification'] = noti_dict
        db1.close()
    return redirect(request.referrer)

@app.route('/all_notifications')
def all_notifications():
    return render_template('all_notifications.html')

@app.route('/')
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
        return redirect(url_for('db_error'))

    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)

    show_ads_list = []
    for ad in ads_list:
        startdate_str = str(ad.get_end_date())
        startdate = dt.strptime(startdate_str, "%Y-%m-%d")
        if startdate >= datetime.now() and ad.get_status() == "Approved":
            show_ads_list.append(ad)

    return render_template('index.html', show_ads_list=show_ads_list)

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
                    error = "Internal error of opening database."

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

                # Cost Calculation
                delta = create_ad.enddate.data - create_ad.startdate.data
                cost = delta.days * 25

                if(create_ad.adtext.data == None):
                    adtext = ' '
                else:
                    adtext = create_ad.adtext.data

                ad = Ads.Ads(str(count_id) + file_extension[1], username, create_ad.startdate.data,
                               create_ad.enddate.data, adtext)
                ad.set_ad_id(count_id)
                ads_dict[ad.get_ad_id()] = ad
                db['Ads'] = ads_dict
                # Test codes
                ad = ads_dict[ad.get_ad_id()]

                db.close()

                return redirect(url_for('manage_ads'))
                #return redirect(url_for('static', filename=backoflink))

    return render_template('advertise.html', form=create_ad, error=error)

@app.route('/manage_ads')
def manage_ads():
    try:
        ads_dict = {}
        db = shelve.open('ads.db', 'w')
        ads_dict = db['Ads']
    except:
        return redirect(url_for('db_error'))

    ads_list = []
    for key in ads_dict:
        ad = ads_dict.get(key)
        ads_list.append(ad)

    count = 0
    expired_list = []
    show_ads_list = []
    for ad in ads_list:
        if username == ad.get_store_name():
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

    if username == "Admin":
        count = len(ads_list)
        show_ads_list = []
        show_ads_list = ads_list

    return render_template('manage_ads.html', count=count, ads_list=show_ads_list, username=username)

@app.route('/updateAd/<int:id>/<int:updatewhat>/', methods=['GET', 'POST'])
def updateAd(id, updatewhat):
    update_ad = UpdateAd(request.form)
    if updatewhat == 1: #Update Status only
        try:
            ads_dict = {}
            db = shelve.open('ads.db', 'w')
            ads_dict = db['Ads']
        except:
            return redirect(url_for('db_error'))
        ad = ads_dict.get(id)
        ad.set_status("Approved")
        create_notification(ad.get_store_name(),"updates","Your advertisement just got approved!", "manage_ads")  # create notification
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
                return redirect(url_for('db_error'))

            ad = ads_dict.get(id)
            ad.set_start_date(update_ad.startdate.data)
            ad.set_end_date(update_ad.enddate.data)
            ad.set_adtext(update_ad.adtext.data)
            if username == "Admin":
                ad.set_status(update_ad.status.data)
                if update_ad.status.data == "Rejected":
                    create_notification(ad.get_store_name(), "updates", "Sorry, your advertisement isn't in-line with our terms and conditions and has been rejected.",
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

            update_ad.adtext.data = ad.get_adtext()
            if username == "Admin":
                update_ad.status.data = ad.get_status()
        return render_template('updateAd.html', form=update_ad, username=username)

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
        db.close()
        return redirect(url_for('manage_ads'))

@app.route('/CustRegister', methods=['GET', 'POST'])
def createcustomeracct():
    createcustacct = createCust(request.form)

    if request.method == 'POST' and createcustacct.validate():
        try:
            custDict = {}
            cdb = shelve.open('cust.db', 'c')
            custDict = cdb['cust']
        except:
            print("error reading cust.db")

        custacct = CustRegister.CustRegister(createcustacct.city.data, createcustacct.email.data,
                                             createcustacct.password.data, createcustacct.firstname.data,
                                             createcustacct.lastname.data, createcustacct.number.data)

        cdb[createcustacct.email.data] = custacct
        cdb['CustRegister'] = custDict

        cdb.close()

        return redirect(url_for('CustLogin'))

    return render_template('CustRegister.html', form=createcustacct)

@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    create_prod = CreateProduct(request.form)
    error = None
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

            count_id = 0
            if username in catalogue_dict: #Set count_id to the max number of the store
                for product in catalogue_dict[username]:
                    if product.get_id() >= count_id:
                        count_id = product.get_id() + 1

            # Image Handling
            app.config['UPLOAD_FOLDER'] = './static/uploads/shops/' + username + '/'
            filename = secure_filename(file.filename)
            pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True) #Create shop directory if does nt exist.
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_extension = os.path.splitext(filename)  # get file type
            os.rename(app.config['UPLOAD_FOLDER'] + filename, app.config['UPLOAD_FOLDER'] +str(count_id) + file_extension[1])
            # End of Image Handling

            qns = ''
            if create_prod.q1.data != '' and len(create_prod.flist1.data) > 1:
                qns = Catalogue.Customiseable(create_prod.q1.data, create_prod.flist1.data, create_prod.q1category.data)

            prod = Catalogue.Catalouge(count_id, create_prod.name.data, create_prod.price.data, create_prod.discount.data,
                                       str(count_id) + file_extension[1], create_prod.description.data, qns)

            if username in catalogue_dict:
                catalogue_dict[username].append(prod)
            else:
                catalogue_dict[username] = [prod]

            db['Catalogue'] = catalogue_dict
            db.close()
            return redirect(url_for('catalogue'))


    return render_template('addproduct.html', form=create_prod, error=error)

@app.route('/catalogue')
def catalogue():
    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error'), errorid=0)

    if username not in catalogue_dict:
        return redirect(url_for('add_product'))

    return render_template('catalogue.html', catalogue_list=catalogue_dict[username], username=username)

@app.route('/deleteProduct/<name>/<int:id>', methods=['POST'])
def delete_product(name, id):
    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'w')
        catalogue_dict = db['Catalogue']
    except:
        return redirect(url_for('general_error'), errorid=0)
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
    if request.method == 'POST' and update_prod.validate():
        try:
            catalogue_dict = {}
            db = shelve.open('catalogue.db', 'w')
            catalogue_dict = db['Catalogue']
        except:
            return redirect(url_for('general_error'), errorid=0)
        for product in catalogue_dict[name]:
            if product.get_id() == id:
                product.set_name(update_prod.name.data)
                product.set_price(update_prod.price.data)
                product.set_discount(update_prod.discount.data)
                product.set_description(update_prod.description.data)
                qns = ''
                if update_prod.q1.data != '' and len(update_prod.flist1.data) > 1:
                    qns = Catalogue.Customiseable(update_prod.q1.data, update_prod.flist1.data,
                                                  update_prod.q1category.data)
                product.set_custom(qns)

                if 'image' not in request.files:
                    error = 'Something went wrong, please refresh page.'
                file = request.files['image']
                if file.filename != '' and not allowed_file(file.filename):
                    error = 'The file format must be in jpg, jpeg, png or gif.'
                # elif update_prod.q1.data != '' and update_prod.q1category.data != 'textbox':
                #     if len(update_prod.flist1.data) < 1:
                #         error = 'Please create at least one choice for each question.'
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
            return redirect(url_for('general_error'), errorid=0)

        for product in catalogue_dict[name]:
            if product.get_id() == id:
                update_prod.name.data = product.get_name()
                update_prod.price.data = product.get_price()
                update_prod.discount.data = product.get_discount()
                update_prod.description.data = product.get_description()

                custom = product.get_custom()
                if custom != '':
                    update_prod.q1.data = custom.get_question()
                    update_prod.q1category.data = custom.get_choices()


    return render_template('updateProduct.html', form=update_prod)

@app.route('/viewshops', methods=['GET' ,'POST'])
def view_shops():
    error = None
    catalogue_dict = {}
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error'), errorid=0)

    shop_dict = {} #Key: [Total Review, Most Discounted Item]
    for key, value in catalogue_dict.items():
        total_review = 0
        best_disc = 0
        for item in value:
            total_review += item.get_reviews()
            if item.get_discount() > best_disc:
                best_disc = item.get_discount()
        shop_dict[key] = [total_review, best_disc]

    search_item = SearchItem(request.form)
    if request.method == 'POST':
        shop_dict = {}
        for key, value in catalogue_dict.items():
            if search_item.search.data != '' and search_item.search.data.lower()[:5] == key.lower()[:5]:
                for item in value:
                    total_review += item.get_reviews()
                    if item.get_discount() > best_disc:
                        best_disc = item.get_discount()
                shop_dict[key] = [total_review, best_disc]

        if not shop_dict: #Checks for empty dict
            error = "Sorry! We could not find the store you are looking for, try searching another store or changing your filter requirements."

        return render_template('viewshops.html', shop_dict=shop_dict, form=search_item, error=error)


    return render_template('viewshops.html', shop_dict=shop_dict, form=search_item, error=error)


@app.route('/view/<name>', methods=['GET', 'POST'])
def viewstore(name):
    catalogue_dict = {}
    disc_price_dict = {}
    try:
        db = shelve.open('catalogue.db', 'r')
        catalogue_dict = db['Catalogue']
        db.close()
    except:
        return redirect(url_for('general_error'), errorid=0)
    #disc_price_dict[item.get_id()] = float(item.get_price()) * ((100 - float(item.get_discount()))/100) #Calculate item discount

    if name not in catalogue_dict:
        return redirect(url_for('view_shops'))

    return render_template('viewstore.html', shop_dict=catalogue_dict[name], name=name)


@app.route('/contact/<name>', methods=['GET', 'POST'])
def contact(name):
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
        if username != "":
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
    if request.method == 'POST':
        chat_dict = {}
        try:
            db = shelve.open('chat.db', 'w')
            chat_dict = db['Chats']
        except:
            return redirect(url_for('general_error'), errorid=0)

        if send_msg.validate():
            if username != "":
                msg_from = username
            else:
                msg_from = chat_dict[chatid].get_sender()

            if chat_dict[chatid].get_sender() == username:
                chat_dict[chatid].set_sender_status("Replied")
                chat_dict[chatid].set_recipient_status("Unreplied")
            else:
                chat_dict[chatid].set_sender_status("Unreplied")

            message = Chat.Message(send_msg.message.data, msg_from, dt.today().strftime("%d %b %Y %H:%M"))
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
            if username == "" and session['temp_user'] != None:
                if chat_dict[item].get_sender() == session['temp_user']:
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            elif chat == "inbox":
                if chat_dict[item].get_sender() == username and chat_dict[item].get_sender_status() != "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
                elif chat_dict[item].get_recipient() == username and chat_dict[item].get_recipient_status() != "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            elif chat == "archive":
                if chat_dict[item].get_sender() == username  and chat_dict[item].get_sender_status() == "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
                elif chat_dict[item].get_recipient() == username  and chat_dict[item].get_recipient_status() == "Archive":
                    user_chat[chat_dict[item].get_id()] = chat_dict[item]
            else:
                return redirect(url_for('general_error', errorid=2))

        if username == "Admin":
            user_chat = chat_dict

    return render_template('chat.html', user_chat=user_chat, chatid=chatid, form=send_msg, username=username)

@app.route('/chat/<action>/<int:id>', methods=['GET', 'POST'])
def update_chatstatus(action, id):
    chat_dict = {}
    try:
        db = shelve.open('chat.db', 'w')
        chat_dict = db['Chats']
    except:
        return redirect(url_for('general_error'), errorid=0)
    else:
        if action == "resolved":
            chat_dict[id].set_recipient_status("Resolved")
        elif action == "delete":
            if username == "Admin":
                chat_dict.pop(id)
            elif username == chat_dict[id].get_recipient:
                chat_dict[id].set_recipient_status("Hidden")
            else:
                chat_dict[id].set_sender_status("Hidden")
        elif action == "archive":
            if username == chat_dict[id].get_recipient:
                chat_dict[id].set_recipient_status("Archive")
            else:
                chat_dict[id].set_sender_status("Archive")

        db['Chats'] = chat_dict
        db.close()

        if action != "archive":
            action = "inbox"
        return redirect(url_for('chat_page', chat=action ,chatid=id))


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
    else:
        title = "Unknown"
        message = "Something went wrong, please try again later."

    return render_template('error.html', title=title, message=message)

###################################RIDERS START##################################################

@app.route('/')
def riders_home():
    login= False
    if 'username' in session:
        login = True
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
        return render_template('register_complete.html')
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
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        for user_id in users_dict:
            user = users_dict.get(user_id)
            if request.form['user-name'] == user.get_user_name() and request.form['user-password'] == user.get_password():
                session['rider_account'] = user.get_user_id()
                return redirect(url_for('riders_home'))
            elif request.form['user-name'] == 'admin' and request.form['user-password'] == 'admin':
                return redirect(url_for('retrieve_riders'))
            else:
                error = 'Invalid Credentials. Please try again.'

    return render_template('login_riders.html', error=error)


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

if __name__ == '__main__':
    app.debug = True
    app.run()
