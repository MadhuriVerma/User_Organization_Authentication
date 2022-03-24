from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))
    username = db.Column(db.String(256))
    mobile_number = db.Column(db.String(256))

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship('OrganizationModel')
   


    def __init__(self,email,password,username,mobile_number,organization_id):
        self.email = email
        self.password = password
        self.username = username
        self.mobile_number = mobile_number
        self.organization_id = organization_id
    

    def json(self):
        return {'email': self.email,'username': self.username,'mobile_number': self.mobile_number, 'organization_id': self.organization_id }    

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod 
    def find_by_email(cls, email):
       return cls.query.filter_by(email = email).first()   

    @classmethod 
    def find_my_mobile_number(cls, mobile_number):
        return cls.query.filter_by(mobile_number = mobile_number).first()

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()