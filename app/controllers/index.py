from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, login_manager
from app.models.tables import User

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('logando')
            return redirect(url_for('pagina_inicial'))
        else:
            flash('login invalido')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))



@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ""

    if request.method == 'POST':
        # db data
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check
        exist_username = User.query.filter_by(username=username).first()
        exist_email = User.query.filter_by(email=email).first()

        if exist_username or exist_email:
            msg = "Username or email already exists. Please choose a different one."
        else:
            # new user
            user = User(name=name, username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return render_template('pagina_inicial.html')

    return render_template('register.html', msg=msg)



@app.route("/pagina_inicial")
def pagina_inicial():
    return render_template('pagina_inicial.html')



@app.route("/profile")
def profile():
    return render_template('profile.html')



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