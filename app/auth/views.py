from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .. import db
from . import auth
from app.models import User
from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ChangePasswordForm, ChangeEmailForm



@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            

            return redirect(url_for('main.add_facility'))
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
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        '''token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)'''
        flash('You have been registered.Login to continue.')
        return redirect(url_for('auth.login'))
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
        '''if user:
            token = user.generate_confirmation_token()
            send_email(
                user.email, 'Reset Your Password', 'auth/email/reset_password',
                user=user, token=token, next=request.args.get('next')
            )
            flash("An email with instructions to reset your password has been sent to you.")
            return redirect(url_for('auth.login'))
        else:
            flash("Unable to find an account associated with that email address")
            return redirect(url_for('auth.password_reset_request'))'''
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

            return redirect(url_for('main.add_assets'))
            
        else:
            flash('Invalid password')
    return render_template('auth/change_password.html', form=form)



@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            '''token = current_user.generate_email_change_token(new_email)
            send_email(
                new_email,
                'Confirm your email address', 'auth/email/change_email',
                user=current_user, token=token
            )'''
            flash("An email with instructions to confirm your new email address " +
                  "has been sent to you.")
            #return redirect(url_for('main.index'))
        else:
            flash("Invalid email or password")
    return render_template('auth/change_email.html', form=form)

