from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)     

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

