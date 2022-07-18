from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from taskManager.models import Users, Customers, Employees, Tasks
from wtforms import ValidationError
from flask_login import login_user, login_required, logout_user, current_user
from taskManager.forms import Loginform, RegistrationForm, CustomersForm, EmployeeForm, TasksForm
from taskManager.extentions import db, login_manager
from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect('data.sqlite3')
c = conn.cursor()
tests = Blueprint('tests', __name__, template_folder='taskManager/templates', static_folder='taskManager/static')


# @tests.route('/pdb')
# def populatedb():
#     db.drop_all()
#     db.create_all()
#     yonatan = Users(firstName="יהונתן", lastName="שטרום", email="yonatan@trot.co.il",password='piano74672@')
#     db.session.add(yonatan)
#     db.session.commit()

@tests.route('/populate')
def populate():
    records = """INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (1, 'יהונתן', 'שטרום', 'yonatan@trot.co.il', '054-8018016');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (2, 'אורטל', 'לוי', 'ortal@trot.co.il', '054-4929329');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (3, 'ניצן', 'בר', 'nitzan@trot.co.il', '054-4328832');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (4, 'ירון', 'כלימיאן', 'yaron@trot.co.il', '054-4819030');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (5, 'אליאל', 'כרמי', 'eliel@trot.co.il', '053-8243355');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (6, 'שי', 'כרמלי', 'shay@trot.co.il', '052-8833989');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (7, 'רועי', 'ארביב', 'roy@trot.co.il', '050-4882345');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (8, 'אופק', 'אלבז', 'ofek@trot.co.il', '050-9511301');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (9, 'עידן', 'בר סבר', 'idan@trot.co.il', '052-3911746');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (10, 'אלכס', 'אבזלמן', 'alex@trot.co.il', '050-6928029');
    INSERT INTO employees_1 (id, firstName, lastName, email, phone) VALUES (11, 'חן', 'גפנר', 'chen@trot.co.il', '054-6395044');
    """
    for line in records:
        return "<h1>{}</h1>".format(line)

    # c.executemany(records)
    # conn.commit()
    # conn.close()


