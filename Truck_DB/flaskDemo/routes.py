import os
import secrets
import mysql.connector
from mysql.connector import Error
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, createForm#, AssignUpdateForm, PostForm, AssignForm
from flaskDemo.models import Customer, Employee, Purchase, Test_Drive, Vehicle
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    display = Vehicle.query.group_by(Vehicle.model).all()
    return render_template('home.html', title='Join', trucks=display)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/join")
def join():
    
    import mysql.connector
    from mysql.connector import Error
    
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                       database='truck',
                                       user='truck',
                                       password='453truck')
        
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT *
                FROM vehicle  
                INNER JOIN purchase  
                ON vehicle.vehicleid = purchase.vehicleid
                WHERE vehicle.vehicleid = 1
                """
                )
            data = cursor.fetchall()

            # Satisfies sqlAlchemy part of 12
            sqldata = Vehicle.query.join(Purchase, Vehicle.vehicleid==Purchase.vehicleid)
            return render_template('Join_2.html', title='Join', data=data, sqldata=sqldata)
    except Error as e:
        print(e)

    finally:
        conn.close()

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
        #Satisfies #9 Filter query
        if form.admin.data:
            user = Employee.query.filter_by(email=form.email.data).first()
        else:
            user = Customer.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
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



@app.route("/create", methods=['GET','POST'])
def create():
    try:
        
        conn = mysql.connector.connect(host='45.55.59.121',
                                        database='truck',
                                        user='truck',
                                        password='453truck')
        
        cursor = conn.cursor()
        print("CONNECTED")
        form = createForm()
        makes = Vehicle.query.with_entities(Vehicle.make).distinct()#possible extra points for distinct dropdown list?
        models = Vehicle.query.with_entities(Vehicle.model).distinct()
        colors = Vehicle.query.with_entities(Vehicle.color).distinct()
        years = Vehicle.query.with_entities(Vehicle.year).distinct()
        if form.validate_on_submit():
            print("in if")
            truck = Vehicle(make = form.make.data, model = form.model.data, color = form.color.data, year = form.year.data)
            make = request.form["make"]
            model = request.form["model"]
            color = request.form["color"]
            year = request.form["year"]
            picture="none.jpg"
            cursor.execute("""INSERT INTO vehicle (make,model,color,year,picture) VALUES (%s, %s,%s,%s,%s)""", (make,model,color,year,picture))
            conn.commit()
            flash('Added truck', 'success')
            return redirect(url_for('home', ))

        
    except Error as e:
        print("error")
        print(e)#possibly delete or implement into the site
    
    finally:
        conn.close()
    return render_template("create_vehicle.html", title = "Create Vehicle", form=form, makes=makes, models=models,colors=colors,years=years)


@app.route("/vehicle/<make>/<model>", methods=['GET','POST'])
#@login_required
def show_vehicle(make, model):
    #truck = Vehicle.query.all() ##FIND
    query = Vehicle.query
    truck = query.filter(Vehicle.model == model).all()
    #vehicle = Vehicle.query.where(Vehicle.model=model).all()
    return render_template('show_vehicle.html', title='Vehicle',
                           truck=truck, legend='Vehicle')

@app.route("/assign/<vehicleid>")
@login_required
def show_by_id(vehicleid):
    assign = Vehicle.query.get_or_404(vehicleid)
    return render_template('vehicle_by_id.html', title="Delete" + str(assign.vehicleid) + ", " + str(assign.model), assign=assign)
  
# 7 Satisfied: Delete one record
@app.route("/vehicle/<vehicleid>/delete", methods=['GET', 'POST'])
@login_required
def delete_vehicle(vehicleid):
    assign = Vehicle.query.get_or_404(vehicleid)
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
        cursor.execute("SELECT * FROM vehicle WHERE vehicleid = 3") #checked and working
        row = cursor.fetchall()
        
        cursor2 = conn.cursor(dictionary=True)
        cursor2.execute("SELECT * FROM vehicle ORDER BY price ASC LIMIT 3")# confirmed working. now uses order by instead of group by
        row2 = cursor2.fetchall()

        cursor3 = conn.cursor(dictionary=True)
        cursor3.execute("SELECT * FROM vehicle WHERE price >105000 AND price < 120000")# confirmed working. now uses order by instead of group by
        row3 = cursor3.fetchall()

        #add 11 satisfaction for sql with a possible drop down menu search for customers
        #with price and make restrictions for example, to make a compound query

        return render_template('show_featured.html', title='Featured Vehicles',row=row,row2=row2,row3=row3)


    except Error as e:
        print(e)#possibly delete or implement into the site

    finally:
        conn.close()
