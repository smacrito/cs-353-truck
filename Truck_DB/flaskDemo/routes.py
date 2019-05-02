import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm #UpdateAccountForm,AssignUpdateForm PostForm,, AssignForm
from flaskDemo.models import Customer, Employee, Purchase, Test_Drive, Vehicle
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    #results = Department.query.all()
    #return render_template('dept_home.html', outString = results)
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    display = Vehicle.query.group_by(Vehicle.model).all()

    #results = Department.query.all()
    #return render_template('dept_home.html', outString = results)
    #posts =  Post.query.all()
    #return render_template('home.html', posts=posts)
    #truckResults = Vehicle.query.get_or_404([make,model])
    return render_template('home.html', title='Join', trucks=display)


   


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
        customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                            password=form.password.data, address=form.address.data)
        db.session.add(customer)
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
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and (customer.password == form.password.data):
            login_user(customer, remember=form.remember.data)
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

#@app.route("/lookup")

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.address.data = current_user.address
    return render_template('account.html', title='Account', form=form)


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
def assign(make, model):
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

@app.route("/vehicle/<make>/<model>", methods=['GET','POST'])
#@login_required
def show_vehicle(make, model):
    truck = Vehicle.query.all() ##FIND
    #vehicle = Vehicle.query.where(Vehicle.model=model).all()
    return render_template('show_vehicle.html', title='Vehicle',
                           truck=truck, legend='Vehicle')

# 7 Satisfied: Delete one record
@app.route("/vehicle/<vehicleid>/delete", methods=['POST'])
#@login_required
def delete_vehicle(vehicleid):
    assign = Vehicle.query.get_or_404([vehicleid])
    db.session.delete(assign)
    db.session.commit()
    flash('The truck has been deleted!', 'success')
    return redirect(url_for('home'))

# 8 Satisfied: Simple SELECT SQL statement; 10 Satisfied: Select aggregate SQL query
@app.route("/show_featured")
#show_featured will show 1 or more featured vehicles, like cheapest, or most luxurious
def show_featured():

    import mysql.connector
    from mysql.connector import Error
    
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                       database='truck',
                                       user='truck',
                                       password='453truck')
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)    # must add vehicle id here or find out how to put variable in for xxxxxx
        #cursor.execute("SELECT * FROM vehicle WHERE vehicleID = x")#extract from form in crud-update
        cursor.execute("SELECT * FROM vehicle WHERE vehicleid = 3 FETCH NEXT 5 ROWS ONLY ") #checked and working
        row = cursor.fetchall()
        
        cursor2 = conn.cursor(dictionary=True)
        cursor2.execute("SELECT vehicle.make, vehicle.price FROM vehicle ORDER BY price ASC")# confirmed working. now uses order by instead of group by
        row2 = cursor2.fetchall()

        #add 11 satisfaction for sql with a possible drop down menu search for customers
        #with price and make restrictions for example, to make a compound query

        return render_template('show_featured.html', title='Featured Vehicles',row=row,row2=row2)


    except Error as e:
        print(e)#possibly delete or implement into the site

    finally:
        conn.close()
