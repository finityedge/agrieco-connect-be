from flask_restful import Resource
from flask import request
from app import db
from app.models import Topic


class TopicsGETResource(Resource):
    def get(self):
        return [topic.serialize() for topic in Topic.query.all()]
    
class TopicResource(Resource):
    def get(self, id):
        topic = Topic.query.get(id)
        if topic:
            return topic.serialize()
        return None
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        new_topic = Topic(name=name, description=description)
        db.session.add(new_topic)
        db.session.commit()
        return new_topic.serialize(), 201
    
    def put(self, id):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        topic = Topic.query.get(id)
        if topic:
            topic.name = name
            topic.description = description
            db.session.commit()
            return topic.serialize()
        return None
    
    def delete(self, id):
        topic = Topic.query.get(id)
        if topic:
            db.session.delete(topic)
            db.session.commit()
            return "", 204
        return None