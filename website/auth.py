from flask import Blueprint, render_template, request, flash

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
            flash("Account Created!", category="pass")
    return render_template('signup.html')
