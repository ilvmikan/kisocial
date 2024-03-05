from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, login_manager
from app.models.tables import User
import os
from .forms import *


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login bem-sucedido', 'success')
            return redirect(url_for('pagina_inicial'))
        else:
            flash('Login inválido. Verifique suas credenciais.', 'error')

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    msg = ""

    if form.validate_on_submit():
        exist_username = User.query.filter_by(username=form.username.data).first()
        exist_email = User.query.filter_by(email=form.email.data).first()
    
        if exist_username or exist_email:
            msg = "Username or email already exists. Please choose a different one."
        else:
            user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form, msg=msg)



@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))
    return render_template('register.html', form=form, msg=msg)