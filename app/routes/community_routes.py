from flask import Blueprint
from flask_restful import Api
from app.resources.community import CommunitiesGETResource, CommunityResource, CommunitiesPOSTResource

bp = Blueprint('community', __name__)
api = Api(bp)

api.add_resource(CommunitiesGETResource, '/communities')
api.add_resource(CommunityResource, '/communities', '/communities/<int:id>')
api.add_resource(CommunitiesPOSTResource, '/communities')