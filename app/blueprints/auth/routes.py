from . import bp as auth
from app import db
from flask import current_app as app, request, url_for, jsonify
from .forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    title = "Eat | Sign Up"
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=username).first():
            message = "That username is taken. Please choose another."
            return jsonify({ 'message': message }), 409
        elif User.query.filter_by(email=email).first():
            message = "That email address is already connected to an account. Please use another."
            return jsonify({ 'message': message }), 409 
        else:
            print(username, email, password)
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            message = "You've successfully signed up. Welcome to EAT!"
            return jsonify({ 'message': message }), 201  # will this lead the user to a deadend page? 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = "EAT | Log In"
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            message = "Email and/or password is not valid. Please try again."
            return jsonify({ 'message': message }), 404

@auth.route('/logout')
def logout():
    logout_user()
    message = "You have logged out. Come back to EAT some more real soon!"    
    return jsonify({ 'message': message }), 201

@auth.route('/myinfo')
@login_required
def myinfo():
    title = "EAT | My Info"
    data = {
        "Username": current_user.username,
        "Email": current_user.email,
        "Password": current_user.password
    }
    return jsonify(data)