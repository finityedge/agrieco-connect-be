from flask_restful import Resource
from flask import request
from app import db
# from app.models import UserFeed

feeds = [{"id": 1, "content": "farmers ai system", "user_id": 1, "created_at": "2021-01-01T00:00:00", "updated_at": "2021-01-01T00:00:00", "images": "https://example.com/image.jpg"},
        {"id": 2, "content": "intelligent vision systems", "user_id": 1, "created_at": "2021-01-01T00:00:00", "updated_at": "2021-01-01T00:00:00", "images": "https://example.com/image.jpg"}]


class FeedsGETResource(Resource):
    def get(self):
        return feeds
    
class FeedResource(Resource):
    def get(self, id):
        for feed in feeds:
            if feed["id"] == id:
                return feed
        return None
    
    def post(self):
        feed = request.json
        new_id = max(feed["id"] for feed in feeds) + 1
        feed["id"] = new_id
        feeds.append(feed)
        return feed
    
    def put(self, id):
        feed = request.json
        for _feed in feeds:
            if _feed["id"] == id:
                _feed.update(feed)
                return _feed
            
    def delete(self, id):
        global feeds
        feeds = [feed for feed in feeds if feed["id"] != id]
        return "", 204
    

    
