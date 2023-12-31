from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
import threading
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"

#DONE: Add a Display to the follower and following list--> Done
#Done: Add a Display to show which bots are yours and from other uers --> Done
#Done: Add to the bot interface a way that the bot gets the posts from the database --> Done
#Done: Add to the bot interface a way that the bot can Comment on posts and get also the comments from the database --> Done
#Done: Add the functinality that mods(admin account) can delete posts and comments --> Done
#Done: Add a algorithm that the posts are sorted by the most likes and current date --> Done
#Done: Add a algorithm that the posts are more personalized for the user on the main page "Home" --> Done

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Winnetou"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from views import views
    from auth import auth
    from Bots_routs import bot_view

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(bot_view, url_prefix='/')

    from models import User, Moderator_Rights

    create_database(app)
    with app.app_context():
        if not User.query.filter_by(email="admin@admin.de").first():
            admin = User(email="admin@admin.de", firstName="admin", password=generate_password_hash("admin", method='sha256'))
            db.session.add(admin)
            db.session.commit()
            mod = Moderator_Rights(user_id=admin.id)
            db.session.add(mod)
            db.session.commit()

    # User loader callback function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Your code here to retrieve the user from the database based on user_id
        return User.query.get(int(user_id))

    return app


def create_database(app):
    db_path = os.path.join(os.getcwd(), DB_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("Created Database!")

app = create_app()


if __name__ == '__main__':
    thread = threading.Thread(target=app.run, kwargs={'host': '192.168.2.33', 'use_reloader': False})
    thread.start()


