
from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegisterForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/login')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registered for user {}'.format(
            form.username.data))
    return render_template('register.html', title='Sign up', form=form)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Penal Berit'}
    transaksasjoner = [
        {
            'sender': {'username': 'John'},
            'mottaker': {'username': 'Grøtta grav'}
        },
        {
            'sender': {'username': 'Susan'},
            'mottaker': {'username': 'Gromlegrau'}
        }
    ]
    return render_template('index.html', title='Home', user=user, transaksasjoner=transaksasjoner)

