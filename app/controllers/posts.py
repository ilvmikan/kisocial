from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from app.models.tables import User, Post

@app.route("/create_post", methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content')

        if content:
            new_post = Post(content=content, user_id=current_user.id)

            try:
                db.session.add(new_post)
                db.session.commit()
                flash('Post created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating post: {str(e)}", 'error')

    return render_template('create_post.html')
