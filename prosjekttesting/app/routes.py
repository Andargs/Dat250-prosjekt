
from app import app, db, mail, limiter, mail_handler
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, EmailVerifForm, TransactionForm
from flask_login import current_user, login_user, login_required, logout_user
from flask import escape, request
import random,string
from flask_mail import Mail, Message
import pyotp
import logging
from app.models import User, Transaction


@app.route('/login', methods=['GET', 'POST'])
#@limiter.limit("200/day")
#@limiter.limit("30/hour")
#@limiter.limit("5/minute")
def login():
    if current_user.is_authenticated:
        return redirect('index/<username>')
    form = LoginForm()
    if form.validate_on_submit():
        u = escape(str(form.username.data))
        p = escape(str(form.password.data))
        user = User.query.filter_by(username=u).first()
        if user is None or not user.check_password(p):
            flash('Invalid username or password')
            app.logger.info(f'{user} failed to log in')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        #return redirect('index')
        return redirect('verification')
    return render_template('login.html', title='Sign In', form=form)
    #return render_template('contact.html')

verified = False
code = ''
@app.route('/verification', methods=['GET', 'POST'])
#@limiter.limit("200/day")
#@limiter.limit("30/hour")
#@limiter.limit("5/minute")
def epostverifisering():
    global code
    global verified
    verified = False
    form = EmailVerifForm()
    if current_user.is_authenticated:
        if request.method=='GET':
            k = pyotp.HOTP('base32secret3232')
            code = k.at(random.SystemRandom().randint(0, 1000000))
            msg = Message("Feedback", recipients=[current_user.email])
            msg.body = "Code:{}\n Use this code to authenticate the user, any other email you may recive from this email is not accociated with skvipps".format(code)
            mail.send(msg)
        else:
            if form.validate_on_submit():
                u = escape(str(form.code.data))
                if u == code:
                    verified = True
                    return redirect('mypage/<username>')
                else:
                    app.logger.info(f'{current_user.username} failed email verification')
                    return redirect('verification')
    else:
        return redirect('login')
    return render_template('contact.html', title='emailverifisering', form=form)



@app.route('/logout')
def logout():
    verified = False
    logout_user()
    return redirect('login')

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('login')
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
    


@app.route('/mypage/<username>', methods=['GET', 'POST']) #index<username>
@login_required
def mypage(username):
    if current_user is None:
        app.logger.info(f'Someone tried to bypass login')
        return redirect('/login')
    if verified == False:
        app.logger.info(f'{username} tried to bypass email verification')
        return redirect('/verification')
    if current_user.username != username:
        app.logger.info(f'{current_user} tried to access {username} account')
        return redirect(url_for('mypage', username=current_user.username))               #index(username)
    if current_user.is_authenticated:
        form = TransactionForm()
    
    #if current_user.username is not index.username:
      #  return redirect(url_for('/mypage', username=current_user.username))
    ##if current_user.is_active is False:
    #    return redirect('login')
    #if current_user.username is not Account.owner_name:
     #   return redirect('index')
    if form.validate_on_submit():
        r = escape(int(form.recieving.data))
        a = escape(int(form.ammount_to_transfer.data))
        s = current_user.id
        sender = User.query.filter_by(id=s).first()
        reciever = User.query.filter_by(id=r).first()
        transaction = Transaction(ammount=a, recieving=r,sender=s)
        if sender.update_balance(a):
            db.session.add(transaction)
            reciever.update_balance(-a)
            db.session.commit()
            app.logger.info(f'{username} transfered {a},- to {reciever.username}')
        else:
            flash("You don't have that amount of money!")
        if type(r) != int:
            app.logger.info(f'{username} failed to transfer money. Plausible injection attempt')
        if type(a) != int:
            app.logger.info(f'{username} failed to transfer money. Plausible injection attempt')
        if type(s) != int:
            app.logger.info(f'{username} failed to transfer money. Plausible injection attempt')
        return redirect('mypage', user=current_user)



        
    return render_template('mypage.html', title='My Page', form=form, user=current_user)

@app.route('/')
@app.route('/index', methods=['GET', 'POST']) 
def index():
    if current_user is None:
        logout()
        return redirect('/index')



    return render_template('index.html', title='Welcome to Skvipps')



