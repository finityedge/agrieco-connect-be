from flask import Blueprint
from flask_restful import Api
from app.resources.auth import LoginResource, RegisterResource

bp = Blueprint('auth', __name__)
api = Api(bp)

api.add_resource(LoginResource, '/auth/login')
api.add_resource(RegisterResource, '/auth/register')


    

