from app import login_manager
from app.models.tables import User

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()




