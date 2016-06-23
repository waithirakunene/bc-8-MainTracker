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
    is_repairperson = db.Column(db.Boolean, default=False)
    

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


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def generate_reset_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    

    

class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(64), unique=True, index=True)
    facility_description= db.Column(db.String(64), unique=True, index=True)
    repairs = db.relationship('Repairs', backref='facility', lazy='dynamic')

class RepairPersons(db.Model):
    __tablename__ = 'repairpersons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    message = db.Column(db.String(120))
    phone_no = db.Column(db.Integer, unique=True) 
    repairs = db.relationship('Repairs', backref='repairpersons', lazy='dynamic')


class RepairStatus:
    NOT_STARTED = 0
    STARTED = 1
    PENDING = 2
    DONE = 3

class Repairs(db.Model):
    __tablename__ = 'repairs'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
   
    requested_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requested_by = db.relationship('User', foreign_keys=[requested_by_id])

    assigned_by_id = db.Column(db.Integer, db.ForeignKey('repairpersons.id'))
    assigned_by = db.relationship('RepairPersons', foreign_keys=[assigned_by_id])


    description = db.Column(db.String(255), nullable=False)
    date_requested = db.Column(db.DateTime(), index=True, default=datetime.now)
    #additional fields
    confirmed = db.Column(db.Boolean, default=False)
    resolved = db.Column(db.Boolean, default=False)
    acknowledged = db.Column(db.Boolean, default=False)
    updated = db.Column(db.DateTime, default=datetime.now)
    progress = db.Column(db.Integer, default=RepairStatus.NOT_STARTED)
    date_requested = db.Column(db.DateTime(), index=True, default=datetime.now)
    date_completed = db.Column(db.DateTime(), nullable=True) 



    @property
    def status(self):
        if self.progress not in (0, 1, 2, 3):
            return "Unknown"
        elif self.progress == RepairStatus.NOT_STARTED:
            return "Not Started"
        elif self.progress == RepairStatus.STARTED:
            return "Started"
        elif self.progress == RepairStatus.PENDING:
            return "In Progress"
        return "DONE"