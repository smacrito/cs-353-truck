import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AssignForm,AssignUpdateForm
from flaskDemo.models import User, Post, Department, Dependent, Dept_Locations, Employee, Project, Works_On
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    #results = Department.query.all()
    #return render_template('dept_home.html', outString = results)
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    results3 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
                .add_columns(Employee.fname, Employee.lname, Works_On.essn, Works_On.pno, Works_On.hours) \
                .join(Project, Works_On.pno == Project.pnumber).add_columns(Project.pname)
    return render_template('assign_home.html', title='Join',joined_m_n=results3)


   


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
        assign = Works_On(essn=form.ssn.data, pno=form.pnumber.data, hours=form.hours.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new assign!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assign.html', title='New Assign',
                           form=form, legend='New Assign')


@app.route("/assign/<pno>/<essn>")
@login_required
def assign(pno, essn):
    assign = Works_On.query.get_or_404([essn,pno])
    return render_template('assign.html', title=str(assign.essn) + "_" + str(assign.pno), assign=assign, now=datetime.utcnow())


@app.route("/assign/<essn>/<pno>/update", methods=['GET', 'POST'])
@login_required
def update_assign(essn,pno):
    assign = Works_On.query.get_or_404([essn,pno])
    currentAssign = assign.pno

    form = AssignUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        assign.essn=form.ssn.data
        assign.pno=form.pnumber.data
        assign.hours=form.hours.data
        db.session.commit()
        flash('Your assign has been updated!', 'success')
        return redirect(url_for('assign', pno=form.pnumber.data, essn=form.ssn.data))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.pnumber.data = assign.pno
        form.ssn.data = assign.essn
        form.hours.data = assign.hours
    return render_template('create_assign.html', title='Update Assign',
                           form=form, legend='Update Assign')


# 7 Satisfied: Delete one record
@app.route("/assign/<vehicleID>/delete", methods=['POST'])
@login_required
def delete_vehicle(vehicleID):
    assign = Vehicle.query.get_or_404([vehicleID])
    db.session.delete(assign)
    db.session.commit()
    flash('The truck has been deleted!', 'success')
    return redirect(url_for('home'))

# 8 Satisfied: Simple SELECT SQL statement
@app.route("/featured/<vehicleID>/", methods=['POST'])
def show_featured(vehicleID):
    conn = mysql.connector.connect(host='45.55.59.121',
                                   database='truck',
                                   user='truck',
                                   password='453truck')
    if conn.is_connected():
        cursor = conn.cursor() # must add vehicle id here or find out how to put variable in for xxxxxx
    cursor.execute("SELECT * FROM vehicle WHERE vehicleID = xxxxxxx")
    row = cursor.fetchone()

    
