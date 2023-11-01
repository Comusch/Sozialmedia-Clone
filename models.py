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
    liked_by_users = db.relationship('User_likes_to_post', back_populates='post')
    hashtags = db.relationship('Post_hashtags', back_populates='post')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, default = 0)
    posts = db.relationship('Post')
    users = db.relationship('User')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    #unique = True means that the email can only be used once
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150), unique = True)
    profile_description = db.Column(db.String(150), default="I am a user of this website!")
    img_profile = db.Column(db.String(150), default = "default.png")
    posts = db.relationship('Post')
    likes_by_users = db.relationship('User_likes_to_post', back_populates='user')

class Moderator_Rights(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.Integer, default = 1)
    user = db.relationship('User')

class Bot_of_User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bot_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    bot = db.relationship('User', foreign_keys=[bot_id])

class Follow_User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower = db.relationship('User', foreign_keys=[follower_id])

class User_likes_to_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    # Define the relationships with User and Post models
    user = db.relationship('User', back_populates='likes_by_users')
    post = db.relationship('Post', back_populates='liked_by_users')

class Post_hashtags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'))

    # Define the relationships with Hashtags and Post models
    post = db.relationship('Post')
    hashtags = db.relationship('Hashtags')

class Hashtags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(150), unique=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    read = db.Column(db.Boolean, default=False)
    img = db.Column(db.String(150), default = "default.png")

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))

    user_to_com = db.relationship('User_to_Com')
    com_to_message = db.relationship('Com_to_Message')

class User_to_Com(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    com_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

class Com_to_Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    com_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    messages = db.relationship('Message')


