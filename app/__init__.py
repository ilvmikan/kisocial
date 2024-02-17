from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app.models.tables import User  # Import your User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.controllers import index