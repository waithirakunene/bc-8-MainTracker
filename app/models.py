from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    assigned_to = db.relationship('RepairRequests', backref='repair_req', lazy='dynamic')
    

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

   

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))    

class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(64), unique=True, index=True)
    facility_description= db.Column(db.String(64), unique=True, index=True)
    repairs = db.relationship('RepairRequests', backref='facility', lazy='dynamic')

class Maintainer(db.Model):
    __tablename__ = 'maintainer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_no = db.Column(db.Integer, unique=True) 
    repairs = db.relationship('RepairAssignments', backref='assignments', lazy='dynamic')

class RepairAssignments(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(120))
    maintainer_id = db.Column(db.Integer, db.ForeignKey('maintainer.id'))
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id'))


class RepairStatus:
    NOT_STARTED = 0
    STARTED = 1
    PENDING = 2
    DONE = 3

class RepairRequests(db.Model):
    __tablename__ = 'repairs'    
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(255), nullable=False)
    date_requested = db.Column(db.DateTime(), index=True, default=datetime.now)
    #additional fields
    confirmed = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Integer, default=RepairStatus.NOT_STARTED)
    date_requested = db.Column(db.DateTime(), index=True, default=datetime.now)
    date_completed = db.Column(db.DateTime(), nullable=True)
    assigned_to = db.relationship('RepairAssignments', backref='repairs', lazy='dynamic')



   