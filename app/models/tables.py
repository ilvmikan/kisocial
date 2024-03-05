from app import db, login_manager
from datetime import datetime, timezone
import pytz



class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    profile_picture = db.Column(db.String(255))
    description = db.Column(db.String(100), default="Não basta conquistar a sabedoria, é preciso usá-la")


    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, password, name, email, profile_picture=None, description=None):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.profile_picture = profile_picture 
        self.description = description if description else "Não basta conquistar a sabedoria, é preciso usá-la"

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
        
    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        self.created_at = datetime.now(timezone.utc)


    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='posts', foreign_keys=user_id, overlaps="author")

    def formatted_date(self):
        now = datetime.utcnow()
        delta = now - self.created_at

        if delta.days == 0:
            brasilia_tz = pytz.timezone('America/Sao_Paulo')
            today_at_brasilia = self.created_at.replace(tzinfo=pytz.UTC).astimezone(brasilia_tz)
            return f'Hoje às {today_at_brasilia.strftime("%H:%M")} (Horário de Brasília)'

    def __repr__(self):
        return "<Post %r>" % self.id
    
class Friends(db.Model):
    __tablename__ = "friends"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)
    friend = db.relationship('User', foreign_keys=friend_id)