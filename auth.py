from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os

auth = Blueprint('auth', __name__)

#TODO: Finish loading the profile image

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data gets the data from the form, form is coming from the login.html post method
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #here is now a cokee about the login
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category="error")
        else:
            flash('This email don\'t exist!', category="error")
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
        if len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(firstName) < 2:
            flash("Email must be greater than 1 characters.", category='error')
        elif password2 != password1:
            flash("Password don\'t match.", category='error')
        elif len(password1) < 4:
            flash("Password is too short.", category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('auth.addProfile'))


    return render_template("signup.html", user=current_user)

@auth.route("/addProfile", methods=['GET', 'POST'])
@login_required
def addProfile():
    if request.method == 'POST':
        print(request.form)
        if request.form.get('image_change') != None:
            print("image_change")
            image = request.files["image_change"]
            print("lol")
            image_filename = f"{current_user.id}_profil.png"
            image_path = os.path.join("static", "Profil_images", image_filename)
            print(image_path)
            image.save(image_path)
            current_user.img_profile = str(current_user.id)+".png"
            print(current_user.img_profile)
            flash("Image saved!", category='success')
        profile_description = request.form.get('profile_description')
        current_user.profile_description = profile_description
        db.session.commit()
        flash("Profile saved!", category='success')
    return render_template("addProfile.html", user=current_user)