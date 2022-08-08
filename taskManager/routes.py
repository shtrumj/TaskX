import flask
from flask import Response, json
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from taskManager.models import Users, Customers, Employees, Tasks, WorkReports, Hypervisor, employees_query, allHypers, HyperSchema, hyper_schema,Servers, Roles,ServersSchema,allServers
from wtforms import ValidationError
import re
from flask_cors import CORS, cross_origin
from taskManager.models import customer_schema
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from taskManager.forms import Loginform, RegistrationForm, CustomersForm, EmployeeForm, TasksForm, HomeSubmit, WorkReportForm, ReportView, HyperVisorForm,InfraView, Mycustomersform, ServersForm
from taskManager.extensions import db, login_manager,api, Resource
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
    return render_template('create/addcustomer.html', form=form, empoloyees=myemp, admin=admin)


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
    email = session['email']
    admin = Users.query.filter_by(email=email).first_or_404()
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
    return render_template('create/addtask.html', form=form, admin=admin)


@main.route('/logout')
def logout():
    logout_user()
    flash("בוצעה התנתקות", category="success")
    return redirect(url_for('main.login'))


@main.route('/report', methods=('GET', 'POST'))
def WorkReport():
    username = session['username']
    form= WorkReportForm()
    email = session['email']
    admin = Users.query.filter_by(email=email).first_or_404()
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
    return render_template('create/WorkReport.html', form=form, admin=admin )

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
        # return f'<h1>{customerid}</h1>'
        choose = Customers.query.filter_by(id=customerid).first()
        customer = choose.name
        # return f'<h1>{customer}</h1>'
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
        serialNumber = str(form.serialNumber.data)
        # return f'<h1> custid is {custid}</h1>'
        new_hypervisor = Hypervisor(customer=customer, ip_address=ip_address, ilo_address=ILO_address, type=type, status=status,
                                    brand=brand, model=model, warranty=warranty, physical_ram_in_GB=physical_ram_in_GB, numberOfProcessors=numberOfProcessors, owner=choose, serialNumber=serialNumber)
        db.session.add(new_hypervisor)
        db.session.commit()
        flash('מארח  נוצר בהצלחה!', category='success')
        return redirect((url_for('main.addHyper')))
    return render_template('create/AddAnHypervisor.html', form=form, customer=mycustomer)


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
    admin = []
    counter = 1
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
        if len(sysadmins)>3:
            return "<h1>Too many admins</h1>"
        for admini in sysadmins:
            admin.append(admini)
        if len(sysadmins) == 3:
            edit_customer = Customers(name=name, city=city, address=address, internalDomain=internalDomain, externalDomain= externalDomain, owaAdd=owaadd , admin1=admin[0], admin2=admin[1], admin3=admin[2])
        if len(sysadmins) == 2:
            edit_customer = Customers(name=name, city=city, address=address, internalDomain=internalDomain,
                                      externalDomain=externalDomain, owaAdd=owaadd, admin1=admin[0], admin2=admin[1])
        if len(sysadmins) == 1:
            Customers(name=name, city=city, address=address, internalDomain=internalDomain,
                      externalDomain=externalDomain, owaAdd=owaadd, admin1=admin[0])

        # return f'<h3>SysAdmin name is {admin[0]} and admin 2 at {admin[1]} and admin3 is {admin[2]}</h3>'
        db.session.merge(edit_customer)
        db.session.commit()
        flash('דוח נשלח בהצלחה!', category='success')
        # db.session.delete(to_delete)
        # db.session.commit()
        return redirect((url_for('main.editcust')))

    return render_template('Edit/EditCustomer.html', form=form, myform=myform, customer=retcustomer, empoloyees=myemp)

@main.route('/TikAtar',methods=('GET','POST'))
def tikview():
    hypers = Hypervisor.query.all()
    retcustomer = Customers.query.all()
    form = Mycustomersform()
    return render_template('views/TikAtar3.html', form=form, customer=retcustomer, hypers=hypers )

@main.route('/AddServer', methods=('GET','POST'))
def addServer():
    roles = Roles.query.all()
    retcustomer = Customers.query.all()
    hypervisors = Hypervisor.query.all()
    form = ServersForm()
    if request.method == 'POST':
        customerid = request.form.get('mycustomer')
        hypervisor = request.form.get('hypervisor')
        ip_address = request.form.get('ip_address')
        sname = request.form.get('name')
        # return f'<h1>Server name is {sname}</h1>'
        osType = request.form.get('osType')
        roles = request.form.getlist('roles')
        full_roles = ' '.join([str(elem) for elem in roles])
        remarks = request.form.get('remarks')
        hyper= Hypervisor.query.filter_by(id=hypervisor).first()
        customerid = hyper.custid
        new_server = Servers(name=sname, ip_address=ip_address, osType=osType, role=full_roles, remarks=remarks, hyper_id= hypervisor, hyper_ip=hyper.ip_address, customer_id=customerid)
        db.session.add(new_server)
        db.session.commit()
        flash('שרת לוגי נוצר בהצלחה!', category='success')
        return redirect((url_for('main.addServer')))

    return render_template('create/AddAServer.html', form=form, customer=retcustomer, hyper=hypervisors, myroles=roles)


@main.route('/it', methods=['GET'])
def api_query():
        all_customers = Customers.query.all()
        return {'data': customer_schema.dump(all_customers)}, 201


@main.route('/hypers', methods=['GET'])
def hyperapi_query():
        mhypers = Hypervisor.query.all()
        return {'data': allHypers.dump(mhypers)},201


@main.route('/servers', methods=['GET'])
def serversapi_query():
        mServers = Servers.query.all()
        return {'data': allServers.dump(mServers)},201


class ServersByID(Resource):
    def get(self,id):
        fields = ['name', 'ip_address']
        byCustomer = Servers.query.filter_by(customer_id=id).all()
        return {'data': allServers.dump(byCustomer)},201


api.add_resource(ServersByID, "/ser/<int:id>")