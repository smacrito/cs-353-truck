from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id)) #customerid

class Customer(db.Model):
    __table__ = db.Model.metadata.tables['customer']

    def __repr__(self):
        return f"Customer('{self.first_name}',{self.last_name}', '{self.email}', '{self.address}')"

    def is_authenticated(self):
        return True

class Employee(db.Model):
    __table__ = db.Model.metadata.tables['employee']

class Purchase(db.Model):
    __table__ = db.Model.metadata.tables['purchase']

class Test_Drive(db.Model):
    __table__ = db.Model.metadata.tables['test_drive']

class Vehicle(db.Model):
    __table__ = db.Model.metadata.tables['vehicle']
