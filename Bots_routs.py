from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, Post, Bot_of_User, Hashtags, Post_hashtags, User_likes_to_post, Comment
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os
import datetime
import json

bot_view = Blueprint('bot_view', __name__)

@bot_view.route("/login_bot/<int:bot_id>", methods=['POST'])
def login_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            login_user(bot, remember=True)
            return "Logged in successfully!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/logout_bot/<int:bot_id>", methods=['POST'])
def logout_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        logout_user()
        return "Logged out successfully!"
    return "This bot don\'t exist!"

def get_hashtags(text):
    hashtags = []
    for word in text.split(" "):
        if word.startswith("#"):
            hashtags.append(word)
    return hashtags

@bot_view.route("/Create_Post_bot/<int:bot_id>", methods=['POST'])
def Create_Post_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            data = request.form.get("post_text")
            hashtags_text = request.form.get("hashtags")
            image_filename = None  # Initialize image filename
            new_Post = Post(text=data, user_id=bot.id)
            db.session.add(new_Post)

            if "image" in request.files:
                image = request.files["image"]
                if image.filename != "":
                    print(str(datetime.datetime.now()) + " " + image.filename)
                    date = str(datetime.datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")
                    image_filename = f"{current_user.id}_{date}.png"
                    image_path = os.path.join("static", "Post_images", image_filename)
                    image.save(image_path)
                    new_Post.post_image = image_filename
            db.session.commit()

            if hashtags_text:
                hashtags = get_hashtags(hashtags_text)
                for hashtag in hashtags:
                    hashtag_id = Hashtags.query.filter_by(hashtag=hashtag).first()
                    if hashtag_id:
                        newPost_hashtag = Post_hashtags(post_id=new_Post.id, hashtag_id=hashtag_id.id)
                        db.session.add(newPost_hashtag)
                    else:
                        newHashtag = Hashtags(hashtag=hashtag)
                        db.session.add(newHashtag)
                        db.session.commit()
                        newPost_hashtag = Post_hashtags(post_id=new_Post.id, hashtag_id=newHashtag.id)
                        db.session.add(newPost_hashtag)
                db.session.commit()
            return "Post created!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/like_post_bot/<int:bot_id>", methods=['POST'])
def like_post_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            post_id = request.form.get("post_id")
            post = Post.query.filter_by(id=post_id).first()
            if post and not User_likes_to_post.query.filter_by(user_id=bot.id, post_id=post.id).first():
                post.likes += 1
                newUser_like_post = User_likes_to_post(user_id=bot.id, post_id=post.id)
                db.session.add(newUser_like_post)
                db.session.commit()
                return "Post liked!"
            return "This post don\'t exist!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/change_Description_bot/<int:bot_id>", methods=['POST'])
def change_Description_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            new_description = str(request.form.get("description"))+" (bot)"
            bot.profile_description = new_description
            db.session.commit()
            return "Description changed!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/get_bot_posts/<int:bot_id>", methods=['POST'])
def get_bot_posts(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            posts = Post.query.order_by(Post.date.desc()).all()
            posts_list = []
            for post in posts:
                post_dict = {}
                post_dict["id"] = post.id
                post_dict["text"] = post.text
                post_dict["likes"] = post.likes
                post_dict["post_image"] = post.post_image
                posts_list.append(post_dict)
            posts_list = json.dumps(posts_list)
            return posts_list
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/get_bot_post/<int:bot_id>", methods=['POST'])
def get_bot_post(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            post_id = request.form.get("post_id")
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post_dict = {}
                post_dict["id"] = post.id
                post_dict["text"] = post.text
                post_dict["likes"] = post.likes
                post_dict["post_image"] = post.post_image
                post_dict = json.dumps(post_dict)
                return post_dict
            return "This post don\'t exist!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/get_bot_comments/<int:bot_id>", methods=['POST'])
def get_bot_comments(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            post_id = request.form.get("post_id")
            post = Post.query.filter_by(id=post_id).first()
            if post:
                comments = Comment.query.filter_by(post_id=post.id).all()
                comments_list = []
                for comment in comments:
                    comment_dict = {}
                    comment_dict["id"] = comment.id
                    comment_dict["text"] = comment.text
                    comment_dict["likes"] = comment.likes
                    comments_list.append(comment_dict)
                comments_list = json.dumps(comments_list)
                return comments_list
            return "This post don\'t exist!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

@bot_view.route("/create_comment_bot/<int:bot_id>", methods=['POST'])
def create_comment_bot(bot_id):
    bot = User.query.filter_by(id=bot_id).first()
    if bot:
        if check_password_hash(bot.password, request.form.get('password')):
            post_id = request.form.get("post_id")
            post = Post.query.filter_by(id=post_id).first()
            if post:
                comment_text = request.form.get("comment_text")
                newComment = Comment(text=comment_text, post_id=post.id)
                db.session.add(newComment)
                db.session.commit()
                return "Comment created!"
            return "This post don\'t exist!"
        else:
            return "Incorrect password, try again."
    return "This bot don\'t exist!"

