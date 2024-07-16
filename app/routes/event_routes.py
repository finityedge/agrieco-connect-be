from flask import Blueprint
from flask_restful import Api
from app.resources.event import EventsGETResource, EventsPOSTResource, EventResource

bp = Blueprint('events', __name__)
api = Api(bp)

api.add_resource(EventsGETResource, '/events')
api.add_resource(EventsPOSTResource, '/events')
api.add_resource(EventResource, '/events', '/events/<int:id>')