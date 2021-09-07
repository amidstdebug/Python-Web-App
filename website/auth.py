from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(
                    'Logged In', category='pass'
                )
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash(
                    'Incorrect password', category='fail'
                )
        else:
            flash(
                'Invalid Email', category='fail'
            )
    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('auth.login')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash(
                'Email Exists!', category='fail'
            )

        elif len(email) < 4:
            flash(
                "Email too short!", category="fail"
            )
        elif len(name) < 1:
            flash(
                "Name too short!", category="fail"
            )
        elif password1 != password2:
            flash(
                "Password not matching!", category="fail"
            )
        elif len(password1) < 7:
            flash(
                "Password too short!", category='fail'
            )
        else:
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(
                "Account Created!", category="pass"
            )
            return redirect(url_for('views.home'))

    return render_template('signup.html')
