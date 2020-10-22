
from app import app, db, mail, limiter, mail_handler, talisman, csrf, login_manager
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, EmailVerifForm, TransactionForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, login_required, logout_user
from flask import escape, request
import random,string
from flask_mail import Mail, Message
import pyotp
import logging
from app.models import User, Transaction
from app.email import send_password_reset_email
from datetime import timedelta


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("200/day")
@limiter.limit("30/hour")
@limiter.limit("5/minute")
@talisman()
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
        return redirect('verification')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/verification', methods=['GET', 'POST'])
#@limiter.limit("200/day")
#@limiter.limit("30/hour")
#@limiter.limit("5/minute")
@talisman()
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
@talisman()
def logout():
    verified = False
    logout_user()
    return redirect('login')

    

@app.route('/register', methods=['GET', 'POST'])
@talisman()
def register():
    flash('Password must have atleast 10 characters, one capital letter, and one integer')
    if current_user.is_authenticated:
        return redirect('login')
    form = RegistrationForm()
    if form.validate_on_submit():
        u = escape(str(form.username.data))
        e = escape(str(form.email.data))
        user = User(username=u, email=e)
        p = escape(str(form.password.data))
        if len(form.password.data) < 10:
            flash('Password must be atleast 10 characters')
            return redirect('/register')
        for bokstav in p:
            stor = bokstav.isupper()
            if stor == True:
                break
            else:
                stor = False
        if stor == False:
            flash('Password must have atleast one capital letter and one integer')
            return redirect('/register')
        for tall in p:
            tall = bokstav.isdigit()
            if tall == True:
                break
            else:
                stor = False
        if tall == False:
            flash('Password must have atleast one capital letter and one integer')
            return redirect('/register')
        user.set_password(p)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)
    


@app.route('/mypage/<username>', methods=['GET', 'POST']) 
@login_required
@talisman()
def mypage(username):
    if current_user is None:
        app.logger.info(f'Someone tried to bypass login')
        return redirect('/login')
    if verified == False:
        app.logger.info(f'{username} tried to bypass email verification')
        return redirect('/verification')
    if current_user.username != username:
        app.logger.info(f'{current_user} tried to access {username} account')
        return redirect(url_for('mypage', username=current_user.username))               
    if current_user.is_authenticated:
        form = TransactionForm()
    if form.validate_on_submit():
        r = escape(str(form.recieving.data))
        a = int(form.ammount_to_transfer.data)
        s = current_user.id
        sender = User.query.filter_by(id=s).first()
        reciever = User.query.filter_by(username=r).first()
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
        return redirect(url_for('mypage', username=current_user.username)) 



        
    return render_template('mypage.html', title='My Page', form=form, user=current_user)

@app.route('/')
@app.route('/index', methods=['GET', 'POST']) 
@talisman()
def index():
    if current_user is None:
        logout()
        return redirect('/index')



    return render_template('index.html', title='Welcome to Skvipps')



@app.before_request
def before_request():
    app.permanent_session_lifetime = timedelta(minutes=3)