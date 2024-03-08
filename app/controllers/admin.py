from app import app, db
from app.models.tables import User, Post

@app.route("/help")
def help():
    commands = [
        "/delete_all_users - Deleta todos os usuários",
        "/delete_all_posts - Deleta todos os posts",
        "/show_all_users - Mostra todos os usuários"
    ]
    return "<br>".join(commands)


@app.route("/delete_all_users", methods=['GET'])
def delete_all_users():
    try:
        db.session.query(User).delete()
        db.session.commit()

        return "All user data deleted successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error deleting user data: {str(e)}"

@app.route("/delete_all_posts", methods=['GET'])
def delete_all_posts():
    try:
        db.session.query(Post).delete()
        db.session.commit()

        return "All Posts data deleted successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error deleting user data: {str(e)}"
    
@app.route("/show_all_users", methods=['GET'])
def show_all_users():
    try:
        users = User.query.all()
        user_data = "<hr>".join([f"Username: {user.username}<br>Senha: {user.password}<br>" for user in users])
        return f"{user_data}"
    except Exception as e:
        return f"Error retrieving user data: {str(e)}"