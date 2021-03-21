from . import bp as auth
from app import db
from flask import current_app as app, request, url_for, jsonify
from .forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

#  Thoughts
    #  Rewatch video on using Postman. See if it's applicable to troubleshoot flask.
    #  Resolve problems with signup. 
    #  Add comments
        #  Test if comments work in Postman

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    title = "Eat | Sign Up"
    form = UserInfoForm()
    data = request.json
    username = form.username.data
    email = form.email.data
    password = form.password.data
    # form.validate_username(username)
    # form.validate_email(email)
    print(request.method)
    print(form.validate())
    print(username, email, password)
    # checks if username is already taken
    # if User.query.filter_by(username=username).first() == username:
    #     message = "That username is taken. Please choose another."
    #     return jsonify({ 'message': message }), 409
    # checks if email is already taken
    # elif User.query.filter_by(email=email).first() == email:
    #     message = "That email address is already connected to an account. Please use another."
    #     return jsonify({ 'message': message }), 409 
    if request.method == 'POST' and form.validate(): 
        p = User(data['username'], data['email'], data['password'])
        print(username, email, password)
        new_user = User(username, email, password)
        db.session.add(p)
        db.session.commit()
        message = "You've successfully signed up. Welcome to EAT!"
        return redirect(url_for('index'))
        return jsonify({ 'message': message })  
        # return jsonify(p.to_dict())
    else:
        return "fail"
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = "EAT | Log In"
    form = LoginForm()

    print(request.method)
    print(form.validate())

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            message = "Email and/or password is not valid. Please try again."    
            return jsonify({ 'message': message }), 404

        return jsonify("good")

    else:
        return jsonify("fail")

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