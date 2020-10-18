from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User, Transaction
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ForgotForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    e_post = StringField('E-mail', validators=[DataRequired()])
    submit = SubmitField('Help me reset my password!')

class TransactionForm(FlaskForm):
    recieving = StringField('Receiver', validators=[DataRequired()])
    ammount_to_transfer = IntegerField('Ammount', validators=[DataRequired()])
    submit = SubmitField('Send')


class EmailVerifForm(FlaskForm):
    code = StringField('Recieved code', validators=[DataRequired()])
    submit = SubmitField('Submit')
