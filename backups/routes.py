from flask import Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from taskManager.models import Users, Customers, Employees, Tasks, WorkReports, Hypervisor
from wtforms import ValidationError
import re
import json
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from taskManager.forms import Loginform, RegistrationForm, CustomersForm, EmployeeForm, TasksForm, HomeSubmit, WorkReportForm, ReportView, HyperVisorForm,InfraView
from taskManager.extentions import db, login_manager
from sqlalchemy.ext.serializer import loads, dumps

from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms_sqlalchemy.fields import QuerySelectField

main = Blueprint('main', __name__, template_folder='taskManager/templates', static_folder='taskManager/static')


@main.route('/', methods=('GET', 'POST'))
@main.route('/login', methods=('GET', 'POST'))
def login():
    user = False
    password = False
    form = Loginform()
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        #password = generate_password_hash(password, 'sha256')
        # form.password.data = ''
        user = Users.query.filter_by(email=email).first()
        if user.check_password(password) and user is not None:
            flash('התחברות בוצעה בהצלחה', category='success')
            login_user(user, remember=False)
            session["username"] = user.firstName
            session["email"] = user.email
            session["userid"] = user.id
            return  redirect('home')
            # next = request.args.get('next')
            # return '<h1>{}</h1>'.format(next)
            # if next == None or not next[0]=='/':
            #     flash('נא להתחבר!', category='danger')
            #     next = url_for('main.home')

            # return redirect(next)
            # return render_template('home.html', user=user)
        else:
            flash('שם משתמש וֿ.או ססמא לא נכונים', category='danger')
            return redirect(url_for('main.login'))

    return render_template('login.html', form=form, user=user, password=password)


@main.route('/reg', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        pass_confirm = form.pass_confirm.data

        def check_email(self, field):
            if Users.query.filter_by(email=field.data).first():
                raise ValidationError('דואר אלקטרוני קיים במערכת')

        new_user = Users(firstName=firstName, lastName=lastName, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('משתמש נוצר בהצלחה!', category='success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/home', methods=('GET', 'POST'))
@login_required
def home():
    form=HomeSubmit()
    if 'username' in session:
        username = session['username']
        email = session['email']
        employeeID = Employees.query.filter_by(email=email).first_or_404()
        tasks = Tasks.query.filter_by(employee_id=employeeID.id).all()
        if request.method == 'POST':
            checks = request.form.getlist('task-checkbox')
            task_to_delete = Tasks.query.filter_by(id=checks[0]).first()
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect(url_for('main.home'))
            return '<h1>{}</h1>'.format(task_to_delete)

    return render_template('home.html', employeeID=employeeID, tasks=tasks, form=form)


@main.route('/addCustomer', methods=('GET', 'POST'))
def addCustomer():
    form = CustomersForm()
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        address = form.address.data
        internalDomain = form.internalDomain.data
        externalDomain = form.externalDomain.data
        owaAdd = form.owaadd.data
        new_customer = Customers(name=name, city=city, address=address, internalDomain=internalDomain,
                                 externalDomain=externalDomain, owaAdd=owaAdd)
        db.session.add(new_customer)
        db.session.commit()
        flash('לקוח נוצר בהצלחה!', category='success')
        return redirect(url_for('main.addCustomer'))
    return render_template('addcustomer.html', form=form)


@main.route('/addEmployee', methods=('GET', 'POST'))
def addEmployee():
    form = EmployeeForm()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        if db.session.query(Employees.email).filter_by(email=email).first():
            flash ("Email Already registered", category="danger")
            return redirect(url_for('main.addEmployee'))
        else:
            phone = form.phone.data
            new_employee = Employees(firstName=firstName, lastName=lastName, email=email, phone=phone)
            db.session.add(new_employee)
            db.session.commit()
            flash('עובד נוצר בהצלחה!', category='success')
            return redirect(url_for('main.addEmployee'))
    return render_template('addsysadmin.html', form=form)


@main.route('/addTask', methods=('GET', 'POST'))
@login_required
def addTask():
    form = TasksForm()
    if form.validate_on_submit():
        description = str(form.description.data)
        customer = str(form.customer.data)
        deadline = str(form.deadline.data)
        dateconvert = datetime.strptime(deadline, '%Y-%m-%d')
        deadline = dateconvert.strftime('%d/%m/%Y')
        status = "משימה פתוחה"
        reportTo = str(form.reportTo.data)
        assignTo = str(form.assignTo.data)
        NassignTo = re.findall('[0-9]+', assignTo)
        NassignToi = [eval(x) for x in NassignTo]
        NassignToirb = NassignToi[0]
        new_task = Tasks(description=description, customer=customer, deadline=deadline, reportTo=reportTo, assignTo=assignTo, employee_id=NassignToirb, status=status)
        db.session.add(new_task)
        db.session.commit()
        flash('משימה נוצרה בהצלחה!', category='success')
        return redirect(url_for('main.addTask'))
    return render_template('addtask.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    flash("בוצעה התנתקות", category="success")
    return redirect(url_for('main.login'))


@main.route('/report', methods=('GET', 'POST'))
def WorkReport():
    username = session['username']
    form= WorkReportForm()
    if form.validate_on_submit():
        customer = str(form.customer.data)
        client= str(form.client.data)
        description = str(form.description.data)
        classification = str(form.classification.data)
        status = str(form.status.data)
        whatHasBeenDone = str(form.whatHasBeenDone.data)
        clientEmailAddress = str(form.clientEmailAddress.data)
        resolve = str(form.resolve.data)
        reason = str(form.reason.data)
        username = session['username']
        new_report = WorkReports(customer=customer, client=client, description=description,classification=classification, resolve=resolve, status=status, reason=reason, whatHasBeenDone=whatHasBeenDone, username=username, clientEmailAddress=clientEmailAddress)
        db.session.add(new_report)
        db.session.commit()
        flash('דוח נשלח בהצלחה!', category='success')
        return redirect((url_for('main.WorkReport')))
    return render_template('WorkReport.html', form=form )

@main.route('/addWorkReport', methods=('GET', 'POST'))
def addWorkReport():
    username = session['username']
    extDomains = Customers.query.all()
    form= WorkReportForm()
    if form.validate_on_submit():
        customer = str(form.customer.data)
        client= str(form.client.data)
        description = str(form.description.data)
        classification = str(form.classification.data)
        status = str(form.status.data)
        whatHasBeenDone = str(form.whatHasBeenDone.data)
        clientEmailAddress = str(form.clientEmailAddress.data)
        resolve = str(form.resolve.data)
        reason = str(form.reason.data)
        username = session['username']
        new_report = WorkReports(customer=customer, client=client, description=description,classification=classification, resolve=resolve, status=status, reason=reason, whatHasBeenDone=whatHasBeenDone, username=username, clientEmailAddress=clientEmailAddress)
        db.session.add(new_report)
        db.session.commit()
        flash('דוח נשלח בהצלחה!', category='success')
        return redirect((url_for('main.WorkReport')))
    return render_template('AddWorkReport.html', form=form, extDomains=extDomains)




@main.route('/Viewreport', methods=('GET', 'POST'))
def ViewWorkReport():
    form= ReportView()
    username = session['username']
    Reports = WorkReports.query.all()
    return render_template('ViewWorkReplorts.html',Reports=Reports, form=form)


@main.route('/AddHypervisor', methods=('GET','POST'))
def addHyper():
    form=HyperVisorForm()
    if form.validate_on_submit():
        customer = str(form.customer.data)
        ip_address = str(form.ip_address.data)
        ILO_address = str(form.ILO_address.data)
        type = str(form.type.data)
        status = str(form.status.data)
        brand = str(form.brand.data)
        model = str(form.model.data)
        warranty = str(form.warranty.data)
        physical_ram_in_GB = str(form.physical_ram_in_GB.data)
        numberOfProcessors = form.numberOfProcessors.data
        new_hypervisor = Hypervisor(customer=customer, ip_address=ip_address, ilo_address=ILO_address, type=type, status=status, brand=brand, model=model, warranty=warranty, physical_ram_in_GB=physical_ram_in_GB, numberOfProcessors=numberOfProcessors)
        db.session.add(new_hypervisor)
        db.session.commit()
        flash('מארח  נוצר בהצלחה!', category='success')
        return redirect((url_for('main.addHyper')))
    return render_template('AddAnHypervisor.html', form=form)


@main.route('/infra',methods=('GET','POST'))
def infrastracture():
    form = InfraView()
    hyper=Hypervisor.query.all()
    serialHyper = dumps(hyper)
    # hyperjson = json.dumps(hyper.t)
    return render_template('CustomerInfrastructure.html', form=form, serialHyper=serialHyper )