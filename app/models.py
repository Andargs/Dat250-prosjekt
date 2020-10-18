from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes
import base64




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Integer, default=100)
    #salt = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        salt = get_random_bytes(8)
        print(salt)
        hash = scrypt(password, salt, 32, 16384, 8, 1)
        basehash = base64.b64encode(hash)
        basehashstring = basehash.decode('utf-8')
        basesalt = base64.b64encode(salt)
        basesaltstring = basesalt.decode('utf-8')
        hashString = "{0};{1};{2};{3};{4}".format(basesaltstring, 16384, 8, 1, basehashstring)
        print(hashString)
        self.password_hash = hashString

    def check_password(self, password):
        hashString = self.password_hash
        deler = hashString.split(";",5)
        saltbyte = bytes(deler[0], 'utf-8')
        salt = base64.b64decode(saltbyte)
        print(salt)
        hash = scrypt(password, salt, 32, 16384, 8, 1)
        basehash = base64.b64encode(hash)
        basehashstring = basehash.decode('utf-8')
        basesalt = base64.b64encode(salt)
        basesaltstring = basesalt.decode('utf-8')
        ny_hashString = "{0};{1};{2};{3};{4}".format(basesaltstring, 16384, 8, 1, basehashstring)
        print(ny_hashString)
        print(hashString)
        if ny_hashString == hashString:
            return True
        else:
            return False
    def get_balance(self):
        return '<Balance: {}'.format(self.balance)
    
    def update_balance(self, ammount):
        if self.balance-ammount < 0:
            return False
        else:
            self.balance -= ammount
            return True 

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    recieving = db.Column(db.Integer)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '{}:{} overførte {},- til {}>'.format(self.timestamp, self.sender, self.ammount_in_transac, self.receiving)
    