
<<<<<<< HEAD
from app import app, db, mail, Message
=======
from app import app, db, mail
>>>>>>> f696bf6587f5b2a59a599c39d5a9353c8cb29e71
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegistrationForm, EmailVerifForm #,TransactionForm
from app.models import User, Transaction, Account
from flask_login import current_user, login_user, login_required, logout_user
<<<<<<< HEAD
from flask import escape
import random,string



=======
from flask import escape, request
import random,string
from flask_mail import Mail, Message
import pyotp
>>>>>>> f696bf6587f5b2a59a599c39d5a9353c8cb29e71


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
        #return redirect('index')
        return redirect('contact')
    return render_template('login.html', title='Sign In', form=form)
    #return render_template('contact.html')

code = ''
@app.route('/contact', methods=['GET', 'POST'])
def epostverifisering():
<<<<<<< HEAD
    
=======
    global code
    form = EmailVerifForm()
>>>>>>> f696bf6587f5b2a59a599c39d5a9353c8cb29e71
    if current_user.is_authenticated:
        #code = str(''.join(random.choice(string.ascii_letters) for _ in range(10)))
       #codo = str(code)
        if request.method=='GET':
            code = str(pyotp.random_base32())
            msg = Message("Feedback", recipients=[current_user.email])
            msg.body = "Code:{}\n Use this code to authenticate the user".format(code)
            mail.send(msg)
        else:
            if form.validate_on_submit():
                u = escape(str(form.code.data))
                if u == code:
                    print('You entered the correct code, you will be transfered shortly')
                    return redirect('index')
                else:
                    return redirect('contact')
                    print('Wrong code, please try again')
    return render_template('contact.html', title='emailverifisering', form=form)



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
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        form = TransactionForm()
    
#    if current_user.is_authenticated:
#        form = TransactionForm(current_user)
    if current_user.id is not Account.id:
        return redirect('logout')
    if form.validate_on_submit():
        r = escape(int(form.receiver.data))
        a = escape(int(form.ammount_to_transfer.data))
        s = escape(int(form.sending.data))
        transaction = Transaction(ammount=a, receiver=r,sender=s)
        Transaction.transaction(a,r,s)
        db.session.add(transaction)
        db.session.commit()
        return redirect('index')

        
    return render_template('index.html', title='Home', form=form)

@app.route('/newaccount', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        form = TransactionForm()
    
    if form.validate_on_submit():
        r = escape(int(form.receiver.data))
        a = escape(int(form.ammount_to_transfer.data))
        s = escape(int(form.sending.data))
        transaction = Transaction(ammount=a, receiver=r,sender=s)
        Transaction.transaction(a,r,s)
        db.session.add(transaction)
        db.session.commit()
        return redirect('index')

        
    return render_template('index.html', title='Home', form=form)


