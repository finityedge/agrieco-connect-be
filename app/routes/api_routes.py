from flask import Blueprint
from flask_restful import Api
from app.resources.feed import FeedResource, FeedsGETResource, FeedCommentsResource, FeedLikesResource

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(FeedsGETResource, '/feeds')
api.add_resource(FeedResource, '/feeds', '/feeds/<int:id>')
api.add_resource(FeedCommentsResource, '/feeds/<int:id>/comments')
api.add_resource(FeedLikesResource, '/feeds/<int:id>/likes')

