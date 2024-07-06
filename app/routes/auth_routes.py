from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from ..models import User, db
from app.resources.auth import LoginResource

bp = Blueprint('auth', __name__)
api = Api(bp)

api.add_resource(LoginResource, '/auth/login')


    

