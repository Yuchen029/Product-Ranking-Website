from flask import render_template, redirect, url_for, flash, session

from myapp import logger
from . import auth
from .. import db
from ..models import User, Product
from .forms import LoginForm, RegistrationForm


# view function for home page
@auth.route('/')
def index():
    product_food = Product.query.filter_by(category="food").order_by(Product.avg_star.desc()).all()
    foods = []
    product_clothes = Product.query.filter_by(category="clothes").order_by(Product.avg_star.desc()).all()
    clothes = []
    product_electronics = Product.query.filter_by(category="electronics").order_by(Product.avg_star.desc()).all()
    electronics = []
    product_sports = Product.query.filter_by(category="sports").order_by(Product.avg_star.desc()).all()
    sports = []
    product_books = Product.query.filter_by(category="books").order_by(Product.avg_star.desc()).all()
    books = []
    product_others = Product.query.filter_by(category="others").order_by(Product.avg_star.desc()).all()
    others = []
    for i in range(0, 5):
        product_food[i].avg_star = round(product_food[i].avg_star)
        foods.append(product_food[i])
        product_clothes[i].avg_star = round(product_clothes[i].avg_star)
        clothes.append(product_clothes[i])
        product_electronics[i].avg_star = round(product_electronics[i].avg_star)
        electronics.append(product_electronics[i])
        product_sports[i].avg_star = round(product_sports[i].avg_star)
        sports.append(product_sports[i])
        product_books[i].avg_star = round(product_books[i].avg_star)
        books.append(product_books[i])
        product_others[i].avg_star = round(product_others[i].avg_star)
        others.append(product_others[i])
    logger.info('this is a info')
    return render_template('auth/index.html', session=session, foods=foods, clothes=clothes, electronics=electronics,
                           sports=sports, books=books, others=others)


# view function for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if the user has logged in, redirect to home page
    if not session.get("ID") is None:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    # if the button is clicked
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # verify password
        if user is not None and user.verify_password(form.password.data):
            flash('log in successfully')
            session["ID"] = user.id
            return redirect(url_for('auth.index'))
        else:
            flash('wrong email or password')
            logger.error('this is a error')
            return redirect(url_for('auth.login'))
    logger.info('this is a info')
    return render_template('auth/login.html', form=form, session=session)


# view function for register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if User.query.filter_by(email=form.email.data).first() is None:
        # if the button is clicked
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            # add user to database
            db.session.add(user)
            db.session.commit()
            flash('You can login now.')
            return redirect(url_for('auth.login'))
    else:
        flash('The email has been registered')
        logger.warn('this is a warn')
    logger.info('this is a info')
    return render_template('auth/register.html', form=form, session=session)


# view function for log out
@auth.route('/logout')
def logout():
    session.pop("ID", None)
    flash('You have been logged out.')
    logger.info('this is a info')
    return redirect(url_for('auth.index'))
