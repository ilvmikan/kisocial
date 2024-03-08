from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app import app, db
from app.models.tables import User, Post

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/pagina_inicial")
@login_required
def pagina_inicial():
    random_posts = Post.query.order_by(db.func.random()).limit(5).all()

    return render_template('pagina_inicial.html', random_posts=random_posts)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        
        users_results = User.query.filter(User.username.ilike(f"%{query}%") | User.name.ilike(f"%{query}%")).all()
        posts_results = Post.query.filter(Post.content.ilike(f"%{query}%")).all()
        
        return render_template('search.html', users_results=users_results, posts_results=posts_results)

    return redirect(url_for('pagina_inicial'))





