from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True,unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    balance = db.Column(db.String(128))
    transactions = db.relationship('Transaction', backref='account')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    receiving = db.Column(db.Integer, db.ForeignKey('account.id'))
    sender = db.Column(db.Integer)
    

    def __repr__(self):
        return '{}:{} overførte {},- til {}>'.format(self.timestamp, self.sender, self.ammount, self.receiving)
    

#class transak(db.Model):
 #   body = db.Column(db.Integer)
  #  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
   # sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    #mottaker = db.Column(db.Integer, db.ForeignKey('user.id'))
#
 #   def __repr__(self):
  #      return '<{}:{} sendte {}kr til {}>'.format(self.timestamp,self.sender,self.body, self.mottaker)

# class transak(db.Model)
#     sum = db.Column(db.Integer, Primary_key=True)
#     sender = db.Column(self.username)
#     mottaker = db.Column(self.username)

#     def __repr__(self):
#        return '{} sendte {}kr til {}'.format(self.sender, self.sum, self.mottaker)

