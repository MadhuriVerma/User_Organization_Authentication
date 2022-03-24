from db import db
from datetime import datetime
class OrganizationModel(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(256))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    users = db.relationship('UserModel', lazy = 'dynamic')


    def __init__(self,organization_name):
        self.organization_name = organization_name
        self.created_at=datetime.now()
       

    def json(self):
        return {'organization_name':self.organization_name, 'users':[user.json() for user in self.users.all()]}    

    @classmethod
    def find_by_name(cls, organization_name):
        return cls.query.filter_by(organization_name=organization_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()