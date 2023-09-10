from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models import Post, User_likes_to_post, Comment, User, Hashtags, Post_hashtags, Follow_User, Bot_of_User, Moderator_Rights
import datetime
from sqlalchemy.sql import func
import Postlike_predictions as post_pred
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
    #Sort posts by the possibility of like and interest of user
    #test of tensor for post
    #get the 4 newest posts
    posts = Post.query.order_by(Post.date.desc()).all()
    #print(post_pred.Calculate_posts_Tensor(posts))
    #print(post_pred.Calculate_user_Tensor(current_user))
    posts_array = post_pred.Create_post_Tensor_Array(posts, current_user)
    posts_array = post_pred.Sort_post_Tensor_Array(posts_array)
    posts_sorted = []
    for post in posts_array:
        posts_sorted.append(post[0])
    #posts = post_pred.predict_posts(posts, current_user.id)
    return render_template("home.html", user=current_user, authorization=Moderator_Rights.query.filter_by(user_id=current_user.id).first(),posts= posts_sorted, hashtags=Hashtags.query.all())

@views.route('/delete-post', methods=['POST'])
def delete_post():
    postj = json.loads(request.data)
    postId = postj['postId']
    post = Post.query.get(postId)
    if post:
        if Moderator_Rights.query.filter_by(user_id=current_user.id).first():
            db.session.delete(post)
            db.session.commit()
            flash("The post was deleted!", category="success")

    return jsonify({})

@views.route('/delete-comment', methods=['POST'])
def delete_comment():
    commentj = json.loads(request.data)
    commentId = commentj['commentId']
    comment = Comment.query.get(commentId)
    if comment:
        if Moderator_Rights.query.filter_by(user_id=current_user.id).first():
            db.session.delete(comment)
            db.session.commit()
            flash("The post was deleted!", category="success")

    return jsonify({})

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
        elif request.form.get("send_comment"):
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
        elif request.form.get("follow"):
            user_to_follow = User.query.filter_by(id=request.form.get("follow")).first()
            if user_to_follow and user_to_follow.id != current_user.id and not Follow_User.query.filter_by(follower_id=current_user.id, followed_person_id=user_to_follow.id).first():
                new_follow = Follow_User(follower_id=current_user.id, followed_person_id=user_to_follow.id)
                db.session.add(new_follow)
                db.session.commit()
                flash(f'Now you follow {user_to_follow.firstName}!', category="success")

    return render_template("Profil.html", user=current_user, other_user=User.query.filter_by(id=user_id).first(), hashtags=Hashtags.query.all(), follower_of_other=Follow_User.query.filter_by(followed_person_id=user_id).all(), following_of_other=Follow_User.query.filter_by(follower_id=user_id).all(), bots=Bot_of_User.query.filter_by(user_id=user_id).all())

@views.route('/Hashtag/<int:hashtag_id>', methods=['GET', 'POST'])
@login_required
def hashtag_side(hashtag_id):
    print(Post.query.join(Post_hashtags).filter(Post_hashtags.hashtag_id == hashtag_id).all())
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
    return render_template("Hashtags.html", user=current_user, hashtag=Hashtags.query.filter_by(id=hashtag_id).first(), hashtags=Hashtags.query.all(), hashtag_posts=Post.query.join(Post_hashtags).filter(Post_hashtags.hashtag_id == hashtag_id).order_by(Post.date.desc()).all())

