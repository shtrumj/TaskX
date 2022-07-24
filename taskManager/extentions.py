from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
CORS()
ma = Marshmallow()
