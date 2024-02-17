from app import db, login_manager

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    profile_picture = db.Column(db.String(255))

    def __init__(self, username, password, name, email, profile_picture=None):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.profile_picture = profile_picture 

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

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id) 

    def __repr__(self):
        return "<Post %r>" % self.id
    
class Friends(db.Model):
    __tablename__ = "friends"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)
    friend = db.relationship('User', foreign_keys=friend_id)