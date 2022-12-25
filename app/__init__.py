import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import basedir, config

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object(config[config_name])
# config[config_name].init_app(app)
db = SQLAlchemy()

# db.init_app(app)
# login_manager.init_app(app)
# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)


# create app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init db and login manager
    db.init_app(app)

    # register blue print
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .load import load as load_blueprint
    app.register_blueprint(load_blueprint)

    return app
