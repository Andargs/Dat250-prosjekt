from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # konto = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

# class transak(db.Model)
#     sum = db.Column(db.Integer, Primary_key=True)
#     sender = db.Column(self.username)
#     mottaker = db.Column(self.username)

#     def __repr__(self):
#        return '{} sendte {}kr til {}'.format(self.sender, self.sum, self.mottaker)

