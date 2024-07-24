from flask_restful import Resource
from flask import request
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity


class UsersGETResource(Resource):
    def get(self):
        return [user.serialize_less_sensitive() for user in User.query.all()]
    
class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return user.serialize_less_sensitive()
        return None
            
    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return "", 204
    
class UserFollowResource(Resource):
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        user = User.query.get(user_id)
        userToFollow = User.query.get(id)
        if user:
            user.followUnfollow(userToFollow)
            return {'message': 'User followed'}, 200
        return {'message': 'User not found'}, 404

class UserFollowingResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        user = User.query.get(user_id)
        
class UserAppointmentsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        
        user = User.query.get(user_id)
        return [appointment.serialize() for appointment in user.appointments]
    
