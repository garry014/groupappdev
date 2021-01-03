from flask import Flask, render_template, request, redirect, url_for, Request
from Forms import *
from cregform import *
import os, pathlib, shelve, Ads, CustRegister, Catalogue
from datetime import datetime as dt
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

username = "Ah Tong Tailor"  #Test Script

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #File upload size cap 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if enddate < datetime.now() and ad.get_status() != "Rejected":
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
                qns = Catalogue.Customiseable(create_prod.q1.data, create_prod.q1category.data, create_prod.flist1.data)

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
        return redirect(url_for('dberror'))

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
        return redirect(url_for('db_error'))
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
            return redirect(url_for('dberror'))
        for product in catalogue_dict[name]:
            if product.get_id() == id:
                product.set_name(update_prod.name.data)
                product.set_price(update_prod.price.data)
                product.set_discount(update_prod.discount.data)
                product.set_description(update_prod.description.data)
                qns = ''
                if update_prod.q1.data != '' and len(update_prod.flist1.data) > 1:
                    qns = Catalogue.Customiseable(update_prod.q1.data, update_prod.q1category.data,
                                                  update_prod.flist1.data)
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
            return redirect(url_for('dberror'))

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
        return redirect(url_for('dberror'))

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
        return redirect(url_for('dberror'))
    #disc_price_dict[item.get_id()] = float(item.get_price()) * ((100 - float(item.get_discount()))/100) #Calculate item discount

    if name not in catalogue_dict:
        return redirect(url_for('view_shops'))

    return render_template('viewstore.html', shop_dict=catalogue_dict[name], name=name)

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