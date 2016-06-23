from flask import render_template, url_for, redirect, request, flash, g
from flask_login import current_user, login_user, login_required, logout_user
from .. import db
from . import auth
from app.models import User
from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ChangePasswordForm



@auth.before_request
def before_request():
    g.user = current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)               
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash("You have been registered. Welcome {}.".format(user.username))
        login_user(user)               
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('This email is already registered.')

def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError("Username is taken")


@auth.route('/reset', methods=['GET', 'POST'])
def reset_password():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')

            return redirect(url_for('main.index'))
            
        else:
            flash('Invalid password')
    return render_template('auth/change_password.html', form=form)



