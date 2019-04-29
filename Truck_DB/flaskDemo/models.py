from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

class Customer(db.Model):
    __table__ = db.Model.metadata.tables['customer']

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id)) #customerid

class Employee(db.Model):
    __table__ = db.Model.metadata.tables['employee']

class Purchase(db.Model):
    __table__ = db.Model.metadata.tables['purchase']

class Test_Drive(db.Model):
    __table__ = db.Model.metadata.tables['test_drive']

class Vehicle(db.Model):
    __table__ = db.Model.metadata.tables['vehicle']
