import flask
from flask import Response, json
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from taskManager.models import Users, Customers, Employees, Tasks, WorkReports, Hypervisor, employees_query, allHypers, HyperSchema
from wtforms import ValidationError
import re
from flask_cors import CORS, cross_origin
from taskManager.models import customer_schema
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from taskManager.forms import Loginform, RegistrationForm, CustomersForm, EmployeeForm, TasksForm, HomeSubmit, WorkReportForm, ReportView, HyperVisorForm,InfraView, Mycustomersform
from taskManager.extensions import db, login_manager
from sqlalchemy.ext.serializer import loads, dumps
from flask_cors import CORS, cross_origin


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
    form = HomeSubmit()
    if 'username' in session:
        username = session['username']
        email = session['email']
        employeeID = Employees.query.filter_by(email=email).first_or_404()
        admin = Users.query.filter_by(email=email).first_or_404()
        tasks = Tasks.query.filter_by(employee_id=employeeID.id, status='משימה פתוחה').all()
        closedTasks = Tasks.query.filter_by(employee_id=employeeID.id, status='משימה נסגרה').limit(3).all()
        # if request.method == 'POST':
        if form.validate_on_submit():
            checks = request.form.getlist('task-checkbox')
            closed = request.form.getlist('closetask-checkbox')
            if not checks and not closed:
                return redirect(url_for('main.home'))
            else:
                if not closed:
                    task_change_status = Tasks.query.filter_by(id=checks[0]).first()
                    task_change_status.status = 'משימה נסגרה'
                    db.session.commit()
                    return redirect(url_for('main.home'))
                    return '<h1>{}</h1>'.format(task_to_delete)
                else:
                    task_change_status = Tasks.query.filter_by(id=closed[0]).first()
                    task_change_status.status = 'משימה פתוחה'
                    db.session.commit()
                    return redirect(url_for('main.home'))
                    return '<h1>{}</h1>'.format(task_to_delete)

    return render_template('home.html', employeeID=employeeID, tasks=tasks, form=form, closedTasks=closedTasks, admin=admin)


@main.route('/addCustomer', methods=('GET', 'POST'))
def addCustomer():
    form = CustomersForm()
    email = session['email']
    myemp = Employees.query.all()
    admin = Users.query.filter_by(email=email).first_or_404()
    sysadmins = request.form.getlist('sysadmins')
    admini = ''
    for admin in sysadmins:
        admini += admin
        if len(list(sysadmins)) > 0:
            admini += ','
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        address = form.address.data
        internalDomain = form.internalDomain.data
        externalDomain = form.externalDomain.data
        owaAdd = form.owaadd.data
        new_customer = Customers(name=name, city=city, address=address, internalDomain=internalDomain,
                                 externalDomain=externalDomain, owaAdd=owaAdd,sysadmins=admini)
        db.session.add(new_customer)
        db.session.commit()
        flash('לקוח נוצר בהצלחה!', category='success')
        return redirect(url_for('main.addCustomer'))
    return render_template('addcustomer.html', form=form, empoloyees=myemp, admin=admin)


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
    mycustomer=Customers.query.all()
    form=HyperVisorForm()
    if form.validate_on_submit():
        customerid = request.form.get('mycustomer')
        choose = Customers.query.filter_by(id=customerid).first()
        customer = choose.name
        # return f'<h1>customer id is {customerid} </h1>'
        ip_address = str(form.ip_address.data)
        ILO_address = str(form.ILO_address.data)
        type = str(form.type.data)
        status = str(form.status.data)
        brand = str(form.brand.data)
        model = str(form.model.data)
        warranty = str(form.warranty.data)
        physical_ram_in_GB = str(form.physical_ram_in_GB.data)
        # custid = request.form.get('selected')
        numberOfProcessors = form.numberOfProcessors.data
        # return f'<h1> custid is {custid}</h1>'
        new_hypervisor = Hypervisor(customer=customer, ip_address=ip_address, ilo_address=ILO_address, type=type, status=status,
                                    brand=brand, model=model, warranty=warranty, physical_ram_in_GB=physical_ram_in_GB, numberOfProcessors=numberOfProcessors, owner=choose)
        db.session.add(new_hypervisor)
        db.session.commit()
        flash('מארח  נוצר בהצלחה!', category='success')
        return redirect((url_for('main.addHyper')))
    return render_template('AddAnHypervisor.html', form=form, customer=mycustomer)


@main.route('/infra',methods=('GET','POST'))
def infrastracture():
    form = InfraView()
    hyper=Hypervisor.query.all()
    serialHyper = dumps(hyper)
    # hyperjson = json.dumps(hyper.t)
    return render_template('CustomerInfrastructure.html', form=form, serialHyper=serialHyper )


@main.route('/mycustomers',methods=('GET','POST'))
def mycustomers():
    form = Mycustomersform()
    hyper = Hypervisor.query.all()
    return render_template('MyCustomers.html', form=form)


@main.route('/editCustomers',methods=('GET','POST'))
def editcust():
    myemp = Employees.query.all()
    myform = Mycustomersform()
    form = CustomersForm()
    retcustomer = Customers.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        address = request.form.get('address')
        internalDomain = request.form.get('internalDomain')
        externalDomain = request.form.get('externalDomain')
        owaadd = request.form.get('owaadd')
        customer_id = request.form.get("cid")
        sysadmins = request.form.getlist('sysadmins')
        admin = {}
        counter = 1
        for admini in sysadmins:
            selectedadmin = Employees.query.filter_by(id=admini).first()
            selectedadminemail = selectedadmin.email
            admin[counter] = selectedadminemail
            counter += 1
        edit_customer = Customers(name=name, city=city, address=address, internalDomain=internalDomain, externalDomain= externalDomain, owaAdd=owaadd , admin1=admin[1], admin2=admin[2], admin3=admin[3])
        return f'<h3>SysAdmin name is {admin[1]} and admin 2 at {admin[2]} and admin3 is {admin[3]}</h3>'
        db.session.merge(edit_customer)
        db.session.commit()
        flash('דוח נשלח בהצלחה!', category='success')
        # db.session.delete(to_delete)
        # db.session.commit()
        return redirect((url_for('main.editcust')))

    return render_template('Edit/EditClients.html', form=form, myform=myform, customer=retcustomer, empoloyees=myemp)

@main.route('/TikAtar',methods=('GET','POST'))
def tikview():
    retcustomer = Customers.query.all()
    form = Mycustomersform()
    return render_template('views/TikAtar.html', form=form, customer=retcustomer )

@main.route('/it', methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_query():
        # result = customers_schema.dumps(all_customers, ensure_ascii=False)
        all_customers = Customers.query.all()
        # almost =jsonify(customer_schema.dump(all_customers))
        # return almost
        return {'data': customer_schema.dump(all_customers)}, 201


@main.route('/hypers', methods=['GET'])
def hyperapi_query():
        mhypers = Hypervisor.query.all()
        return {'data': allHypers.dump(mhypers)},201




