from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models import Post
import datetime
from sqlalchemy.sql import func
import json
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, posts= Post.query.order_by(Post.date.desc()).all())

@views.route('/Create_Post', methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "POST":
        print(request.form)
        data = request.form.get("post_text")
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
            flash('Post is saved!', category="success")

    return render_template("Creating_Post.html", user=current_user)
