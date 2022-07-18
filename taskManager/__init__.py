from flask import Flask, Blueprint
from flask_session import Session
from flask_migrate import Migrate
from .extentions import db, migrate, login_manager
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from taskManager.routes import main
from taskManager.tests import tests
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'xncv bjhbhdskc9iu3egbcikeniolwer'
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)
    login_manager.init_app(app)
    app.register_blueprint(tests)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    login_manager.login_view = 'main.login'
    return app