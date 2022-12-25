from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# user database to store user information
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    products = db.relationship('Product', backref='seller', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    # generate password hash
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # verify password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# product database to store product information
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(32), index=True)
    description = db.Column(db.String(128), index=True)
    image = db.Column(db.String(256), index=True)
    price = db.Column(db.Float, index=True)
    avg_star = db.Column(db.Float, index=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feedbacks = db.relationship('Feedback', backref='rated', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.name)


# feedback database to store feedback information
class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    star = db.Column(db.Integer, index=True)
    comment = db.Column(db.String(140), index=True)
    time = db.Column(db.String, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return '<Feedback {}>'.format(self.comment)


# # decorator
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
