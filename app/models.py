from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def compare(object1, object2):
    for value in[prop for prop in object1.dict if prop!= '_sa_instance_state' and prop!= 'id']:
        if object1.__dict__.get(value) != object2.__dict__.get(value):
            return False
    return True

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique= True, nullable = False)
    admin = db.Column(db.Boolean, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password_hash = db.Column(db.String(), nullable = False)

    def repr(self):
        return f'<User: {self.username}'
    
    def to_dict(self):
        return {'username': self.username, 'email': self.email}
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #These two functions are used in tandem, to avoid storing plaintext passwords. 
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




ALLOWED_STATES = {'NJ'}

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    zipcode = db.Column(db.Integer, nullable = False)
    state  = db.Column(db.String(2), nullable = False)
    city = db.Column(db.String(25), nullable = False)
    #The Google Places ID, used for easier navigation when available. 
    placeId = db.Column(db.String, unique = True)
    
    def __repr__(self):
        return f'(Address: {self.number} {self.name}, {self.city}, {self.state}. Zip: {self.zipcode})'
    def commit(self):
        if self.state in ALLOWED_STATES:
            db.session.add(self)
            db.session.commit()
        else:
            print("Error: State Code Not Permitted")

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
class EmergRoom(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(2), nullable=False)
    address = db.Column(db.Integer, db.ForeignKey('address.id'), nullable = False)
    phone = db.Column(db.String(12), nullable = True)
    website = db.Column(db.String(100), unique = True)




    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#This is the only upload to the database that non-authorized accounts can perform;
#It must be approved by an authorized account before it will be properly processed by the database. 
        
class Pending(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(150), nullable = False)
    street_number = db.Column(db.Integer, nullable = False)
    street_name = db.Column(db.String(150), nullable = False)
    city = db.Column(db.String(150), nullable = False)
    zipcode = db.Column(db.Integer, nullable = False)
    phone_number= db.Column(db.String(12), nullable = True)
    state = db.Column(db.String(20), nullable = False)
    website = db.Column(db.String(150), nullable = True)
    uploader = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "street_number": self.street_number,
                "street_name": self.street_name,
                "city": self.city,
                "zipcode": self.zipcode,
                "phone_number": self.phone_number,
                "state": self.state,
                "website": self.website,
                "uploader": self.uploader}
    
    def commit(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


#Used for tracking changes to the database. 
class Update_Log(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    #Type of log entry.
    #1: Entry Change, 2: deletion, 3: confirmation
    entry_type = db.Column(db.Integer, nullable = False)
    data = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable = False)

    def commit(self):
        self.date = date.today()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()