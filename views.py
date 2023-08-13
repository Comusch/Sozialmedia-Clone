from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models import Post, User_likes_to_post, Comment, User, Hashtags, Post_hashtags
import datetime
from sqlalchemy.sql import func
import json
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        print(request.form)
        id_like = request.form.get("like")
        if id_like:
            post = Post.query.filter_by(id=id_like).first()
            if post:
                post.likes += 1
                newUser_like_post = User_likes_to_post(user_id=current_user.id, post_id=id_like)
                db.session.add(newUser_like_post)
                db.session.commit()
                flash('Post is liked!', category="success")
        else:
            comment_texts = request.form.getlist("comment_text")
            comment_text = ""
            for comment_txt in comment_texts:
                if comment_txt != "":
                    comment_text = comment_txt
            id_post = request.form.get("send_comment")
            if len(comment_text) < 1:
                flash('Comment is too short!', category="error")
            else:
                new_comment = Comment(text=comment_text, user_id=current_user.id, post_id=id_post)
                db.session.add(new_comment)
                db.session.commit()
                flash('Comment is saved!', category="success")
    return render_template("home.html", user=current_user, posts= Post.query.order_by(Post.date.desc()).all(), hashtags=Hashtags.query.all())

def get_hashtags(text):
    hashtags = []
    for word in text.split(" "):
        if word.startswith("#"):
            hashtags.append(word)
    return hashtags

@views.route('/Create_Post', methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "POST":
        print(request.form)
        data = request.form.get("post_text")
        hashtags_text = request.form.get("hashtags")
        if len(data) < 1:
            flash('Post is too short!', category="error")
        else:
            image_filename = None  # Initialize image filename
            new_Post = Post(text=data,  user_id=current_user.id)
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

            flash('Post is saved!', category="success")

    return render_template("Creating_Post.html", user=current_user)



@views.route('/Profil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profil(user_id):
    if request.method == "POST":
        comment_texts = request.form.getlist("comment_text")
        comment_text = ""
        for comment_txt in comment_texts:
            if comment_txt != "":
                comment_text = comment_txt
        id_post = request.form.get("send_comment")
        if len(comment_text) < 1:
            flash('Comment is too short!', category="error")
        else:
            new_comment = Comment(text=comment_text, user_id=current_user.id, post_id=id_post)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment is saved!', category="success")
    return render_template("Profil.html", user=current_user, other_user=User.query.filter_by(id=user_id).first())