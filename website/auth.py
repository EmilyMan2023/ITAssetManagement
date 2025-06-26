from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# blueprint to group authentication routes
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form data 
        email = request.form.get('email')
        password = request.form.get('password')

        # look up user email
        user = User.query.filter_by(email=email).first()
        if user:
            # verify password
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')

        else:
            flash('Email does not exist', category='error')    

    # GET request - render login page
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # end session
    logout_user()
    # redirect to login page
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        department = request.form.get('department')
        # should be 'regular' or 'admin'
        role = request.form.get('role') 

        # validation checks
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 6:
            flash('Password must be greater than 5 characters.', category='error')
        elif len(department) < 2:
            flash('Department must be greater than 1 character.', category='error')
        elif role not in ['user', 'admin']:
            flash('Invalid role selected.', category='error')
        else:
            # create new user with hashed password
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                department=department,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            # auto-login after signup
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # GET request - show signup form
    return render_template("sign-up.html", user=current_user)
