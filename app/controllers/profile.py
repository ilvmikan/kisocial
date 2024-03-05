from flask import render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from app import app, db
from app.models.tables import User
import os
from .forms import EditProfileForm
from werkzeug.utils import secure_filename
from .utils import allowed_file


@app.route("/profile/")
@app.route("/profile/<username>")
@login_required
def profile(username=None):
    if username:
        user = User.query.filter_by(username=username).first()

        if not user:
            abort(404)
    else:
        user = current_user

    return render_template('profile.html', user=user, is_owner=(user == current_user))



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
            
        if form.description.data:
            current_user.description = form.description.data


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
