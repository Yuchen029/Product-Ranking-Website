import os
import datetime

from flask import render_template, redirect, url_for, send_from_directory, request, session

from werkzeug.utils import secure_filename

from . import load
from .. import db
from ..models import Product, Feedback, User
from .forms import ProductForm, CommentForm, PriceForm

# upload directory
UPLOAD_FOLDER = './app/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# view function for display all products for one category
@load.route('/display_product/<cat>', methods=['GET', 'POST'])
def display_product(cat):
    if session.get("ID") is None:
        return redirect(url_for('auth.index'))
    priceForm = PriceForm()
    lowPrice = priceForm.lowPrice.data
    highPrice = priceForm.highPrice.data
    products = Product.query.filter_by(category=cat).all()
    pls = []
    count = 1
    if lowPrice is None or highPrice is None:
        allProduct = Product.query.filter_by(category=cat).all()
        for p in allProduct:
            p.avg_star = round(p.avg_star)
            pls.append(p)
            # add gap for each 3 products
            if count % 3 == 0:
                pls.append(" ")
            count += 1
    elif priceForm.validate_on_submit():
        product = Product.query.filter(
            (Product.price >= lowPrice) & (Product.price <= highPrice) & (Product.category == cat)).all()
        for p in product:
            p.avg_star = round(p.avg_star)
            pls.append(p)
            # add gap for each 3 products
            if count % 3 == 0:
                pls.append(" ")
            count += 1
    food = Product.query.filter_by(category='food').count()
    clothes = Product.query.filter_by(category='clothes').count()
    electronics = Product.query.filter_by(category='electronics').count()

    sports = Product.query.filter_by(category='sports').count()
    books = Product.query.filter_by(category='books').count()
    others = Product.query.filter_by(category='others').count()
    return render_template('load/display_product.html', pls=pls, food=food, clothes=clothes, electronics=electronics,
                            books=books,  sports=sports, others=others, priceForm=priceForm)


# view function to search product
@load.route('/search_product/<name>', methods=['GET', 'POST'])
def search_product(name):
    if session.get("ID") is None:
        return redirect(url_for('auth.login'))
    products = Product.query.filter_by(name=name).all()
    pls = []
    count = 1
    for p in products:
        p.avg_star = round(p.avg_star)
        pls.append(p)
        # add gap for each 3 products
        if count % 3 == 0:
            pls.append(" ")
        count += 1
    return render_template('load/search_product.html', pls=pls)


# view function to redirect to the product detail
@load.route('/product_details/<p>', methods=['GET', 'POST'])
def product_details(p):
    form = CommentForm()
    user = User.query.filter_by(id=session.get("ID")).first()
    if request.method == 'POST':
        time = datetime.datetime.now()
        t = "{}-{}-{} {}:{}:{}".format(time.year, time.month, time.day, time.hour, time.minute, time.second)
        feedback = Feedback(username=user.username, star=form.star.data, comment=form.comment.data, product_id=p, time=t)
        db.session.add(feedback)
        db.session.commit()
        redirect(url_for('load.product_details', p=p))
    product = Product.query.filter_by(id=p).first()
    feedbacks = Feedback.query.filter_by(product_id=p).all()
    star = [0, 0, 0, 0, 0]
    if len(feedbacks) != 0:
        for feedback in feedbacks:
            if feedback.star == 1:
                star[0] += 1
            elif feedback.star == 2:
                star[1] += 1
            elif feedback.star == 3:
                star[2] += 1
            elif feedback.star == 4:
                star[3] += 1
            else:
                star[4] += 1
        avg_star = (star[0] + 2 * star[1] + 3 * star[2] + 4 * star[3] + 5 * star[4]) / len(feedbacks)
        stars = round(avg_star)
        product.avg_star = avg_star
        db.session.commit()
        last_feedback = feedbacks[len(feedbacks) - 1]
    else:
        stars = 0
        last_feedback = None
    return render_template('load/product_details.html', form=form, session=session, p=product, feedbacks=feedbacks,
                           feedback_num=len(feedbacks), last_feedback=last_feedback, stars=stars, star=star)


# view function for view all products uploaded by the user
@load.route('/view_product', methods=['GET', 'POST'])
def view_product():
    if session.get("ID") is None:
        return redirect(url_for('auth.login'))
    products = Product.query.filter_by(user_id=session.get("ID")).all()
    pls = []
    count = 1
    for p in products:
        p.avg_star = round(p.avg_star)
        pls.append(p)
        # add gap for each 3 products
        if count % 3 == 0:
            pls.append(" ")
        count += 1
    food = Product.query.filter_by(category='food', user_id=session.get("ID")).count()
    clothes = Product.query.filter_by(category='clothes', user_id=session.get("ID")).count()
    electronics = Product.query.filter_by(category='electronics', user_id=session.get("ID")).count()
    medicine = Product.query.filter_by(category='medicine', user_id=session.get("ID")).count()
    books = Product.query.filter_by(category='books', user_id=session.get("ID")).count()
    sports = Product.query.filter_by(category='sports', user_id=session.get("ID")).count()
    life = Product.query.filter_by(category='life', user_id=session.get("ID")).count()
    others = Product.query.filter_by(category='others', user_id=session.get("ID")).count()
    return render_template('load/view_product.html', pls=pls, food=food, clothes=clothes, electronics=electronics,
                           medicine=medicine, books=books, life=life, sports=sports, others=others)


# set allowed file limit for upload file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# create upload file directory
@load.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# view function for upload product
@load.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if session.get("ID") is None:
        return redirect(url_for('auth.index'))
    form = ProductForm()
    if request.method == 'POST':
        file = request.files['file']
        print("y")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save product
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_url = url_for('load.uploaded_file', filename=filename)
            product = Product(name=form.name.data, category=form.category.data, description=form.description.data,
                              image="../../static" + file_url, price=form.price.data, user_id=session.get("ID"))
            # add product to database
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('auth.index'))
    return render_template('load/add_product.html', form=form)
