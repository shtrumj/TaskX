import app
from .extensions import db, login_manager,ma
from flask_login import UserMixin
from datetime import datetime
from marshmallow import Schema, fields
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import Schema, fields, ValidationError, pre_load
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import ARRAY

def employees_names_query():
    query = Employees.query.all()
    return query


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


EmployeeSysadmin = db.Table('EmployeeSysadmin',
                            db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
                            db.Column('customer_id', db.Integer, db.ForeignKey('customers.id'))
                            )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.TEXT)
    lastName = db.Column(db.TEXT)
    email = db.Column(db.TEXT, unique=True)
    password_hash = db.Column(db.TEXT)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, firstName, lastName, email, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password_hash = generate_password_hash(password, 'sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.TEXT)
    lastName = db.Column(db.TEXT)
    email = db.Column(db.String(25), unique=True)
    phone = db.Column(db.TEXT)
    customer = db.relationship('Customers', secondary=EmployeeSysadmin, backref='administrators')
    # tasks = db.relationship('Tasks', backref='employee', lazy=True)

    def __init__(self, firstName, lastName, email, phone):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone

    def __repr__(self):
        return str(self.id) + ".  " + self.firstName + " " + str(self.lastName)


class Servers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(20), nullable=False)
    ip_address = db.Column(db.String(20))
    osType = db.Column(db.String(20))
    role = db.Column(db.String(150))
    hyperid = db.Column(db.Integer, db.ForeignKey('hypervisor.id'))


class Hypervisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.Column(db.String(20))
    ip_address = db.Column(db.String(20))
    type = db.Column(db.String(30))
    status = db.Column(db.String(25))  # active /not active
    ilo_address = db.Column(db.String(20))
    brand = db.Column(db.String(15))
    model = db.Column(db.String(15))
    warranty = db.Column(db.String(15))
    physical_ram_in_GB = db.Column(db.String(15))
    numberOfProcessors = db.Column(db.String(10))
    custid = db.Column(db.Integer, db.ForeignKey('customers.id'))
    servers = db.relationship('Servers', backref='hypervisor')
    def __init__(self, customer, ip_address, type, status, ilo_address, brand, model, warranty, physical_ram_in_GB,
                 numberOfProcessors, owner):
        self.customer = customer
        self.ip_address = ip_address
        self.type = type
        self.status = status
        self.ilo_address = ilo_address
        self.brand = brand
        self.model = model
        self.warranty = warranty
        self.physical_ram_in_GB = physical_ram_in_GB
        self.numberOfProcessors = numberOfProcessors
        self.owner =owner

class HyperSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hypervisor
hyper_schema = HyperSchema(many=True)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    city = db.Column(db.String(10))
    address = db.Column(db.String(20))
    internalDomain = db.Column(db.String(15))
    externalDomain = db.Column(db.String(20))
    owaAdd = db.Column(db.String(20))
    admin1 = db.Column(db.String(30))
    admin2 = db.Column(db.String(30), nullable=True)
    admin3 = db.Column(db.String(30), nullable=True)
    hypervisors = db.relationship('Hypervisor', backref='owner')

    def __init__(self, name, city, address, internalDomain, externalDomain, owaAdd, admin1, admin2,admin3):
        self.name = name
        self.city = city
        self.address = address
        self.internalDomain = internalDomain
        self.externalDomain = externalDomain
        self.owaAdd = owaAdd
        self.admin1 = admin1
        self.admin2 = admin2
        self.admin3 = admin3

    def __repr__(self):
        return self.name

    # Customers Schema


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
customer_schema = CustomerSchema(many=True)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignTo = db.Column(db.String(20))
    description = db.Column(db.String(20))
    customer = db.Column(db.String(100))
    deadline = db.Column(db.String(12))
    reportTo = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    status = db.Column(db.String(20), nullable=True, default="פתוח")

    def __init__(self, assignTo, description, customer, deadline, reportTo, employee_id, status):
        self.assignTo = assignTo
        self.description = description
        self.customer = customer
        self.deadline = deadline
        self.reportTo = reportTo
        self.employee_id = employee_id
        self.status = status


class WorkReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.Column(db.String(20))
    client = db.Column(db.String(20))
    description = db.Column(db.String(30))
    status = db.Column(db.String(25))
    classification = db.Column(db.String(20))
    resolve = db.Column(db.String(150))
    reason = db.Column(db.String(150))
    username = db.Column(db.String(25))
    whatHasBeenDone = db.Column(db.String(150))
    clientEmailAddress = db.Column(db.String(30))

    def __init__(self, customer, client, description, classification, resolve, status, reason, whatHasBeenDone,
                 username, clientEmailAddress):
        self.customer = customer
        self.client = client
        self.description = description
        self.classification = classification
        self.status = status
        self.resolve = resolve
        self.reason = reason
        self.username = username
        self.clientEmailAddress = clientEmailAddress
        self.whatHasBeenDone = whatHasBeenDone


def customer_query():
    query = db.session.query(Customers).all()
    return query


def my_customer_query():
    query = db.session.query(Customers.administrators).all()
    return query


def bosses_names_query():
    query = db.session.query(Employees).all()
    return query

def employees_query():
    query = db.session.query(Employees).all()
    return query




class HyperSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Hypervisor
allHypers = HyperSchema(many=True)
