from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField, DateField, SelectField, TextAreaField,IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, length, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from taskManager.models import customer_query, employees_names_query, bosses_names_query,my_customer_query
import taskManager.routes
# from taskManager.models import Employees

class Loginform(FlaskForm):
    email = StringField("כתובת דואר אלקטרוני", validators=[DataRequired(), Email()])
    password = PasswordField('סיסמא', validators=[DataRequired()])
    submit = SubmitField('שליחה')


class RegistrationForm(FlaskForm):
    firstName = StringField("שם פרטי")
    lastName = StringField("שם משפחה")
    email = StringField("כתובת דואר אלקטרוני")
    password = PasswordField('סיסמא',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='ססמאות חייבות להיות זהות')])
    pass_confirm = PasswordField('אימות סיסמא', validators=[DataRequired()])
    submit = SubmitField('הירשמו')


class CustomersForm(FlaskForm):
    name = StringField("שם הלקוח")
    city = StringField("עיר")
    address = StringField("כתובת")
    internalDomain = StringField("דומיין פנימי")
    externalDomain = StringField("דומיין חיצוני")
    owaadd = StringField("כתובת OWA")
    submit = SubmitField('יצירת לקוח')
    sysadmins = StringField('ניהול רשת')

class EmployeeForm(FlaskForm):
    firstName = StringField("שם פרטי")
    lastName = StringField("שם משפחה")
    email = StringField("כתובת דואר אלקטרוני")
    phone = StringField("מספר טלפון נייד")
    submit = SubmitField('הוספת מנהל רשת')


class TasksForm(FlaskForm):
    assignTo = QuerySelectField('אחראי משימה' ,query_factory=employees_names_query, allow_blank=True)
    description = StringField('תאור המשימה')
    customer = QuerySelectField('שם הלקוח', query_factory=customer_query, allow_blank=True)
    deadline = DateField('תאריך יעד')
    reportTo = QuerySelectField('ממנה משימה', query_factory=bosses_names_query, allow_blank=True)
    submit = SubmitField('צור משימה')


class HomeSubmit(FlaskForm):
    submit = SubmitField('עדכון')


class ReportView(FlaskForm):
    submit = SubmitField('עדכון')


class WorkReportForm(FlaskForm):
    customer = QuerySelectField('שם הלקוח', query_factory=customer_query, allow_blank=True)
    client = StringField('שם המשתמש')
    clientEmailAddress = StringField('כתובת דואר משתמש ארגונית')
    description = StringField('תאור הקריאה')
    classification = SelectField('סוג התקלה', choices=[('בעיית תוכנה','בעיית תוכנה'),('בעיית חומרה','בעיית חומרה')])
    status = SelectField('סטטוס', choices=[('1','טרם החל טיפול'),('2', 'בעיה נפתרה'), ('3', 'בעיה בטיפול')])
    resolve= TextAreaField('תיאור הפתרון')
    reason= TextAreaField('סיבה')
    whatHasBeenDone = TextAreaField('מה נעשה עד כה ?')
    submit = SubmitField('שלח דוח')


class HyperVisorForm(FlaskForm):
    customer = QuerySelectField('שם הלקוח', query_factory=customer_query, allow_blank=True)
    ip_address = StringField('כתובת IP')
    ILO_address = StringField('כתובת ILO')
    type = SelectField('סוג המארח', choices=[('1', 'Proxmox'), ('2', 'Hyper-V'), ('3', 'VMware')])
    status = SelectField('סטטוס', choices=[('1','פעיל'),('2','מיועד לכיבוי'),('3','כבוי')])
    brand = SelectField('יצרן',choices=[('1','HP'),('2','Dell'),('3','Lenovo')])
    model = SelectField('דגם', choices=[
        ('1','DL360'),
        ('2','DL380'),
        ('3','ML350'),
        ('4','PowerEdge R630'),
        ('5','PowerEdge R430'),
        ('6','PowerEdge T440')])
    warranty = DateField('תאריך פקיעת אחריות')
    physical_ram_in_GB = IntegerField('כמות זכרון פיזי ב GB')
    numberOfProcessors = StringField('מספר מעבדים')
    serialNumber = StringField('מספר סידורי')
    submit = SubmitField('מארח חדש')


class ServersForm(FlaskForm):
    name = StringField('שם השרת')
    ip_address = StringField('כתובת IPv4')
    osType = SelectField('סוג מערכת הפעלה', choices=[('1', 'Windows'), ('2', 'Linux')])
    remarks = StringField('הערות')
    submit = SubmitField('שרת חדש')


class InfraView(FlaskForm):
    customer = QuerySelectField('שם הלקוח', query_factory=customer_query, allow_blank=True)
    submit = SubmitField('בחרתי לקוח')


class Mycustomersform(FlaskForm):
    mycustomer = QuerySelectField('בחרו לקוח', query_factory=customer_query, allow_blank=True)