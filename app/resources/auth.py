from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from app import db
from app.models import User, Topic

users = [{"id": 1, "username": "user1", "email": "test@email.com" , "password": "password"},
        {"id": 2, "username": "user2", "email": "test2@email.com", "password": "password"}]

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        # user = next((user for user in users if user["username"] == username), None)
        # if user and user.check_password(password):
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return  {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401
    
class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        fullname = data.get('fullname')
        email = data.get('email')
        interested_topics_ids = data.get('interested_topics_ids')
        password = data.get('password')

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        new_user = User(fullname=fullname, username=username, email=email, password=password)
        if interested_topics_ids:
            interested_topics = Topic.query.filter(Topic.id.in_(interested_topics_ids)).all()
            new_user.interested_topics.extend(interested_topics)

            # topics = Topic.query.filter(Topic.id.in_(interested_topics_ids)).all()
            # new_user.interested_topics = topics

            
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
    
def check_if_user_is_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    return user.role == 'admin'