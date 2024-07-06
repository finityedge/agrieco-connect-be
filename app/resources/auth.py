from flask_restful import Resource
from flask import request
from app import db
# from app.models import User

users = [{"id": 1, "username": "user1", "email": "test@email.com" , "password": "password"},
        {"id": 2, "username": "user2", "email": "test2@email.com", "password": "password"}]

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # user = User.query.filter_by(username=username).first()
        user = next((user for user in users if user["username"] == username), None)
        # if user and user.check_password(password):
        if user and user["password"] == password:
            return {"message": "Login successful"}, 200
        return {"message": "Invalid credentials"}, 401
    
# class RegisterResource(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
#             return {"message": "User already exists"}, 400

#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         return {"message": "User registered successfully"}, 201