
from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import current_user, login_user, login_required


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registered for user {}'.format(
            form.username.data))
    return render_template('register.html', title='Sign up', form=form)

@app.route('/')
@app.route('/index')
#@login_required
def index():
    if 1 == 1:
        transaksasjoner=[]
        user = 1
        return render_template('index.html', title='Home', transaksasjoner=transaksasjoner)

