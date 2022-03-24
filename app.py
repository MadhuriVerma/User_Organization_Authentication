from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import User
from resources.user import UserList
from resources.organization import Organization
from resources.organization import OrganizationList
from resources.organization import CreateOrganization
from resources.user import UserRegister
from resources.organization import EditOrganization
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'madhuri'

api = Api(app)

db.init_app(app)
with app.app_context():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Organization, '/organization')   
api.add_resource(User,'/user')
api.add_resource(UserList, '/users')  
api.add_resource(OrganizationList, '/organizations')
api.add_resource(CreateOrganization,'/create_organization')  
api.add_resource(UserRegister,'/register_user')
api.add_resource(EditOrganization,'/edit_organization')
   

if __name__ == '__main__':
    app.run(port=5000, debug=True)
