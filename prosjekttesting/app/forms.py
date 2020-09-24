from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    e_post = Stringfield('E-mail', validators=[Datarequired()])
    submit = SubmitField('Register')

class ForgotForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    e_post = StringField('E-mail', validators=[Datarequired()])
    submit = SubmitField('Help me reset my password!')

class TransactionForm(FlaskForm):
    receiver = StringField('Receiver', validators=[DataRequired()])
    ammount = IntField('Ammount', validators=[DataRequired()])
    # From account: drop-down-meny med 