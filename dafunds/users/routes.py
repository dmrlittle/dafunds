# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, request, flash, Blueprint
from dafunds.users.forms import RegistrationFrom, LoginForm
from dafunds.models import User
from dafunds import db,bcrypt
from flask_login import login_user, logout_user, login_required

users_ = Blueprint('users', __name__)

@users_.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationFrom()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users_.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Opening the Gate ... Welcome {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('others.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',form=form,title='Login')

@users_.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('others.home'))
