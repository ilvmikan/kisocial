from flask import render_template, request
from app import app, db
from app.models.tables import User

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


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