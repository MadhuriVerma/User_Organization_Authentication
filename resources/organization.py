from flask_restful import Resource,reqparse
from models.organization import OrganizationModel
from datetime import datetime

class Organization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('organization_id', 
     type=int,
     required=True,
     help="This field cannot be left blank"
    )

    def get(self):
         data = Organization.parser.parse_args()
         organization = OrganizationModel.find_by_id(data['organization_id'])
         if organization:
             return organization.json()
         return {'message': 'Organization not found'},404


class CreateOrganization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('organization_name',
     type=str,
     required=True,
     help="This field cannot be left blank"
    )

    def post(self):
        data = CreateOrganization.parser.parse_args()

        if OrganizationModel.find_by_name(data['organization_name']):
             return {"message":"Organization already exists"}

        organization = OrganizationModel(**data)

        organization.save_to_db()
       
        return {"message":"Organization registered successfully"}   

class OrganizationList(Resource):
    def get(self):
        return {'organizations': [organization.json() for organization in OrganizationModel.query.all()]}


class EditOrganization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('organization_id', 
     type=int,
     required=True,
     help="This field cannot be left blank"
    )
    parser.add_argument('organization_name', 
     type=str,
    #  required=True,
     help="This field cannot be left blank"
    )

    def put(self):
         data = EditOrganization.parser.parse_args()

         organization = OrganizationModel.find_by_id(data['organization_id'])
         if organization:
            try:
                organization.organization_name = data['organization_name']
                organization.updated_at = datetime.now()
                organization.save_to_db()
                return f"Your Organization successfully updated", 200
            except:
                return {"msg": "Please provide name to be edited."}

         else:
            organization = OrganizationModel(data['organization_name'])

            organization.save_to_db()
          
            return {"message":"Organization registered successfully"}  