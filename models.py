from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(150))
    post_image = db.Column(db.String(150), default = "default.png")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, default = 0)
    users = db.relationship('User')
    comments = db.relationship('Comment')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, default = 0)
    dislikes = db.Column(db.Integer, default = 0)
    posts = db.relationship('Post')
    users = db.relationship('User')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    #unique = True means that the email can only be used once
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    profile_description = db.Column(db.String(150), default="I am a user of this website!")
    img_profile = db.Column(db.String(150), default = "default.png")
    posts = db.relationship('Post')
