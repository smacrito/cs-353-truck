from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Customer, Employee, Purchase, Test_Drive, Vehicle #updated to Models
from wtforms.fields.html5 import DateField

import datetime #for year validation /AS

#****************************************************************************** /AS
# Register, Login, Post Truck (edit/delete too), Schedule test drive, Search Truck

trucks = Vehicle.query.with_entities(Vehicle.make).distinct()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

#****************************************************************************** /AS
class PostTruck(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), year_check) #year_check used here
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')

    def year_check(form,field):
        now = datetime.datetime.now()
        current_year = now.year
        
        if len(field.data) != 4 and field.data > (current_year + 1) or field.data < 1900:
            raise ValidationError('Not a valid year.')

class SearchTruck(FlaskForm):
    make_list

#****************************************************************************** /AS   
class AssignUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    #essn = HiddenField("")

#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
    #employee = SelectField("Employee", choices=myChoices)  # myChoices defined at top
    #project = SelectField("Project", project_choices=myProjectChoices)

    #hours = IntegerField("Hours", validators=[DataRequired()])
# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
#    mgr_start = DateField("Manager's Start Date")

#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')

    ssn = SelectField("Employee", choices=myChoices)
    pnumber = SelectField("Project Number", coerce=int, choices=myProjectChoices)
    hours = DecimalField("Hours", places=1, validators=[DataRequired()])

    submit = SubmitField('Update this assign')


# got rid of def validate_dnumber

#   def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#         dept = Department.query.filter_by(dname=dname.data).first()
#         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#             raise ValidationError('That department name is already being used. Please choose a different name.')


class AssignForm(AssignUpdateForm):

    submit = SubmitField('Add this assignment')

#    def validate_essn(self, dnumber):    #because dnumber is primary key and should be unique
#        dept = Department.query.filter_by(dnumber=dnumber.data).first()
#        if dept:
#            raise ValidationError('That department number is taken. Please choose a different one.')

