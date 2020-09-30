
from app import app, db
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegistrationForm, TransactionForm
from app.models import User, Transaction, Account
from flask_login import current_user, login_user, login_required, logout_user



        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        u = escape(str(form.username.data))
        p = escape(str(form.password.data))
        user = User.query.filter_by(username=u).first()
        if user is None or not user.check_password(p):
            flash('Invalid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('index')
    form = RegistrationForm()
    if form.validate_on_submit():
        u = escape(str(form.username.data))
        e = escape(str(form.email.data))
        user = User(username=u, email=e)
        p = escape(str(form.password.data))
        user.set_password(p)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/index', methods=['GET', ])
@login_required
def index():
    
    form = TransactionForm(current_user)
    if form.validate_on_submit():
        r = escape(int(form.receiver.data))
        a = escape(int(form.ammount_to_transfer.data))
        s = escape(int(form.sending.data))
        transaction = Transaction(receiving=r,ammount=a,sender=s)
        db.session.add(transaction)
        db.session.commit()
        flash('Transfer complete')
        return redirect('index')

        
    return render_template('index.html', title='Home')



