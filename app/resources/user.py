from flask_restful import Resource
from flask import request
from app import db
# from app.models import User

users = [{"id": 1, "username": "user1", "email": "test@email.com", "password": "password"},
        {"id": 2, "username": "user2", "email": "test2@email.com", "password": "password"}]


class UsersGETResource(Resource):
    def get(self):
        return users
    
class UserResource(Resource):
    def get(self, id):
        for user in users:
            if user["id"] == id:
                return user
        return None
    
    def post(self):
        user = request.json
        new_id = max(user["id"] for user in users) + 1
        user["id"] = new_id
        users.append(user)
        return user
    
    def put(self, id):
        user = request.json
        for _user in users:
            if _user["id"] == id:
                _user.update(user)
                return _user
            
    def delete(self, id):
        global users
        users = [user for user in users if user["id"] != id]
        return "", 204