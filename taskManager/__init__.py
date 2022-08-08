from flask import Flask, Blueprint
from flask_session import Session
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from .extensions import db, migrate, login_manager, CORS, cross_origin, ma, api
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from taskManager.routes import main
from taskManager.tests import tests
from flask_cors import CORS


import os

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, "Database", 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'xncv bjhbhdskc9iu3egbcikeniolwer'
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    app.register_blueprint(main)
    login_manager.init_app(app)
    api.init_app(app)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    app.register_blueprint(tests)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['JSON_AS_ASCII'] = False
    Session(app)
    ma.init_app(app)
    login_manager.login_view = 'main.login'
    return app
