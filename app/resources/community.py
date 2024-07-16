from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Community

class CommunitiesGETResource(Resource):
    def get(self):
        return [community.serialize() for community in Community.query.all()]
    
class CommunitiesPOSTResource(Resource):
    def post(self):
        result = jwt_required()(self._post)()  # Applying decorator directly and calling wrapped method
        return result

    def _post(self):
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            location = data.get('location')
            category = data.get('category')
            new_community = Community(name=name, description=description, location=location, category=category, user_id=user_id)
            db.session.add(new_community)
            db.session.commit()
            return new_community.serialize(), 201
        except Exception as e:
            print("Error: ", e)
            return {"message": "Invalid request"}, 400
        
class CommunityResource(Resource):
    def get(self, id):
        community = Community.query.get(id)
        if community:
            return community.serialize()
        return None
    
    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            community = request.json
            _community = Community.query.get(id)
            if _community:
                if _community.user_id != user_id:
                    return {"message": "You are not authorized to perform this action"}, 403
                _community.name = community["name"]
                _community.description = community["description"]
                _community.location = community["location"]
                _community.category = community["category"]
                db.session.commit()
                return _community.serialize()
            return None
        except Exception as e:
            print("Error: ", e)
            return {"message": "Invalid request"}, 400
        
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        community = Community.query.get(id)
        if community:
            if community.user_id != user_id:
                return {"message": "You are not authorized to perform this action"}, 403
            db.session.delete(community)
            db.session.commit()
            return "", 204
        return None