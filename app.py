from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

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

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User

    create_database(app)

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
    app.run(host="192.168.2.33")
