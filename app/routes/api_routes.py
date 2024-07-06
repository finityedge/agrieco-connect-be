from flask import Blueprint
from flask_restful import Api
from app.resources.feed import FeedResource, FeedsGETResource

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(FeedsGETResource, '/feeds')
api.add_resource(FeedResource, '/feeds', '/feeds/<int:id>')

