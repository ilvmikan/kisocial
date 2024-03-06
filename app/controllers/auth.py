from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.models.tables import User
from app.controllers.forms import *

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    username = form.username.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return redirect(url_for('pagina_inicial'))

    return render_template('login.html', form=form, show_alert=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    exist_username = User.query.filter_by(username=form.username.data).first()
    exist_email = User.query.filter_by(email=form.email.data).first()

    if exist_username or exist_email:
        return render_template('register.html', form=form, show_alert=True)

    user = User(name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data)
    
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
