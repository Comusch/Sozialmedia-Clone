from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models import Post
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, posts= Post.query.all())

@views.route('/Create_Post', methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "POST":
        data = request.form.get("post_text")
        if len(data)< 1:
            flash('Post is too short!', category="error")
        else:
            new_Post = Post(text=data, user_id=current_user.id)
            db.session.add(new_Post)
            db.session.commit()
            flash('Post is saved!', category="success")
    return render_template("Creating_Post.html", user=current_user)

