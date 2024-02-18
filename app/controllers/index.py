from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.models.tables import User
import os
from .forms import *
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')




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




@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))




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



@app.route("/pagina_inicial")
@login_required
def pagina_inicial():
    return render_template('pagina_inicial.html')




@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)




@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditProfileForm()

    exist_username = User.query.filter_by(username=form.username.data).first()
    exist_email = User.query.filter_by(email=form.email.data).first()
    

    if form.validate_on_submit():

        # trocar de username (caso não exista)
        if form.username.data:
            if exist_username is not None and current_user.username != exist_username.username:
                return redirect(url_for('editar_perfil'))
            current_user.username = form.username.data

        # trocar de email (caso não exista)
        if form.email.data:
            if exist_email is not None and current_user.email != exist_email.email:
                return redirect(url_for('editar_perfil'))
            current_user.email = form.email.data

        # trocar de nome
        if form.name.data:
            current_user.name = form.name.data

        # lógica para foto de perfil
        if form.foto_perfil.data:
            foto_perfil = form.foto_perfil.data
            
            # apagar a foto antiga do db e colocar a nova
            if foto_perfil.filename:
                if current_user.profile_picture:
                    foto_anterior_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_picture)
                    if os.path.exists(foto_anterior_path):
                        os.remove(foto_anterior_path)

                # verificar arquivo
                if allowed_file(foto_perfil.filename):
                    filename = secure_filename(foto_perfil.filename)
                    foto_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    current_user.profile_picture = filename
                else:
                    flash('Tipo de arquivo não permitido para a foto do perfil', 'danger')

        # finish
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile'))

    return render_template('editar_perfil.html', form=form, user=current_user)








@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    # insert
    # i = User("teste", "1234", "Mateus Dias", "teste.dias@gmail.com")
    # db.session.add(i)
    # db.session.commit()

    r = User.query.filter_by(username="mattshr").first()
    print(r.username, r.name)
    return "OK"

# ###########################################
# ###########################################
# ##########        WARNING        ##########
# ###########################################
# ###########################################

@app.route("/delete_all_users", methods=['GET'])
def delete_all_users():
    try:
        db.session.query(User).delete()
        db.session.commit()

        return "All user data deleted successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error deleting user data: {str(e)}"