from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.user import UserModel
import re
from models.organization import OrganizationModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', 
     type=int,
     required=True,
     help="This field cannot be left blank"
     )
    parser.add_argument('organization_name', 
     type=str,
     required=False,
     help="This field cannot be left blank"
     )
   
    @jwt_required()
    def get(self):
        data = User.parser.parse_args()
        user = UserModel.find_by_id(data['id'])
            
        if user:
             org = OrganizationModel.find_by_id(user.organization_id)
             return {'organization': org.organization_name} 
        else:    
             return {'message': 'user not found'},404
           
       
  

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', 
     type=str,
     required=True,
     help="This field cannot be left blank"
     )
    parser.add_argument('password', 
     type=str,
     required=True,
     help="This field cannot be left blank"
     )
    parser.add_argument('username', 
     type=str,
     required=True,
     help="This field cannot be left blank"
     )
    parser.add_argument('mobile_number', 
     type=str,
     required=True,
     help="This field cannot be left blank"
     )   
    parser.add_argument('organization_id', 
     type=int,
     required=True,
     help="Every item needs a store id"
     )

    def post(self):
        data = UserRegister.parser.parse_args()

        try:
            if OrganizationModel.find_by_id(data['organization_id']):
                pass
            else:
              return {"Error": "Organization not found. Please enter a valid organization_id"}
        except:
             return {"Error": "Organization not found. Please enter a valid organization_id"}

        if UserModel.find_by_username(data['username']):
              return {"message": "A user with that username already exists"}, 400
        
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"},400
        else:
            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

            if email_regex.match(data['email']):
                pass
            else:
                return {"Error":"Please enter a valid email address"}

        if UserModel.find_my_mobile_number(data['mobile_number']):
            return {"message": "A user with that number already exists"},400   
        else:
            number = re.fullmatch('[6-9][0-9]{9}',data['mobile_number'])

            if number != None:
                pass
            else:
                return {"message": "Please enter a valid mobile number"},400

        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User registered successfully"} ,201 


class UserList(Resource):
    def get(self):
      return {'users': [x.json() for x in UserModel.query.all()]} 
                         
