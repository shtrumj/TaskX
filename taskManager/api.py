from flask import Flask, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


# https://towardsdev.com/create-a-rest-api-in-python-with-flask-and-sqlalchemy-e4839cd61ddd

api = Blueprint('api', __name__ )

