from datetime import datetime
from time import time
from app import app, db, login_manager
from flask_login import UserMixin
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes
import base64
import jwt



from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine



secret_key = '\x9f\xd5\xfef\x98\xf14_M\x99$\x11=T\xccgx\xf5\xd5\xc0\xc2\xf9\xdc\x1d' 



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(EncryptedType(db.String, secret_key, AesEngine, 'pkcs5'), index=True, unique=True)
    email = db.Column(EncryptedType(db.String, secret_key, AesEngine, 'pkcs5'), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(EncryptedType(db.Integer, secret_key, AesEngine, 'pkcs5'), default=100)
    #salt = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        salt = get_random_bytes(8)
        hash = scrypt(password, salt, 32, 16384, 8, 1)
        basehash = base64.b64encode(hash)
        bas
        ehashstring = basehash.decode('utf-8')
        basesalt = base64.b64encode(salt)
        basesaltstring = basesalt.decode('utf-8')
        hashString = "{0};{1};{2};{3};{4}".format(basesaltstring, 16384, 8, 1, basehashstring)
        self.password_hash = hashString

    def check_password(self, password):
        hashString = self.password_hash
        deler = hashString.split(";",5)
        saltbyte = bytes(deler[0], 'utf-8')
        salt = base64.b64decode(saltbyte)
        hash = scrypt(password, salt, 32, 16384, 8, 1)
        basehash = base64.b64encode(hash)
        basehashstring = basehash.decode('utf-8')
        basesalt = base64.b64encode(salt)
        basesaltstring = basesalt.decode('utf-8')
        ny_hashString = "{0};{1};{2};{3};{4}".format(basesaltstring, 16384, 8, 1, basehashstring)
        if ny_hashString == hashString:
            return True
        else:
            return False


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

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


if __name__ == '__main__':
    db.create_all()