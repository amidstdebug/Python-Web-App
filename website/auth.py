from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email too short!", category="fail")
        elif len(name) < 1:
            flash("Name too short!", category="fail")
        elif password1 != password2:
            flash("Password not matching!", category="fail")
        elif len(password1) < 7:
            flash("Password too short!", category='fail')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created!", category="pass")
            return redirect(url_for('views.home'))

    return render_template('signup.html')
