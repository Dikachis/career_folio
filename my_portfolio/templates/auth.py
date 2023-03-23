from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from my_portfolio import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # user = User.query.filter_by(email=email).first()
        # if user:
            # flash('Email does not exist.', category='error')
        # cur = mysql.connection.cursor()
        
        if len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('password don\'t match', category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(first_name=first_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            # cur.execute("INSERT INTO users(id, first_name, email, password) VALUES(%d, %s, %s, %s)", (id, first_name, email, password))
            # mysql.connection.commit()
            # cur.close()
            try:
                db.session.commit()
            except Exception:
                flash('Account created!', category='success')
                # to redirect the user to homepage  
                return redirect(url_for('auth.login'))
                # return redirect(url_for('views.home'))

    return render_template("sign up.html")