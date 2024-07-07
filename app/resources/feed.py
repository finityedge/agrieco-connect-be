from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.resources.auth import check_if_user_is_admin
from app import db
from app.models import Feed, Topic, User
import os
import re

# Configure Flask-Uploads
# photos = UploadSet('photos', IMAGES)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Configure the upload set to save uploaded files to a specific directory
UPLOAD_FOLDER = 'static/uploads/feed_images'
# configure_uploads(app, photos)

def secure_filename(filename):
    filename = re.sub(r'[^A-Za-z0-9_.-]', '_', filename)
    return filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FeedsGETResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        # i want to return all feeds sorted by date in descending order if user is not logged in and logged in user we only return feeds that are associated with the topics they are interested in
        user_id = get_jwt_identity()
        if user_id:
            user = User.query.get(user_id)
            topics = user.interested_topics
            feeds = Feed.query.filter(Feed.topics.any(Topic.id.in_([topic.id for topic in topics]))).order_by(Feed.created_at.desc()).all()
        else:
            feeds = Feed.query.order_by(Feed.created_at.desc()).all()
        return [feed.serialize() for feed in feeds]
        
    
class FeedResource(Resource):
    def get(self, id):
        feed = Feed.query.get(id)
        if feed:
            return feed.serialize()
        return None
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        
        # Check if files are in the request
        if 'photo' not in request.files:
            return {"message": "No file part"}, 400
        
        photos = request.files.getlist('photo')  # Retrieve list of uploaded files
        
        # Ensure the upload folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Initialize list to store file paths
        uploaded_files = []
        
        for photo in photos:
            if photo.filename == '':
                return {"message": "No selected file"}, 400
            
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(file_path)
                uploaded_files.append(file_path)
        
        # Handle other form data
        content = request.form.get('content')
        topics_str = request.form.get('topics')
        
        # Split the topics string by commas and convert to integers
        topics_ids = [int(topic_id.strip()) for topic_id in topics_str.split(',')] if topics_str else []
        
        new_feed = Feed(content=content, user_id=user_id, images=",".join(uploaded_files))
        
        # Associate topics with the feed
        if topics_ids:
            topics = Topic.query.filter(Topic.id.in_(topics_ids)).all()
            new_feed.topics.extend(topics)
        
        db.session.add(new_feed)
        db.session.commit()
        
        return new_feed.serialize(), 201

    
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        
        feed = request.json
        _feed = Feed.query.get(id)

        if _feed:
            if _feed.user_id != user_id:
                return {"message": "You are not authorized to perform this action"}, 403
            _feed.content = feed["content"]
            _feed.user_id = user_id
            _feed.images = feed["images"]
            if "topics" in feed:
                topics = Topic.query.filter(Topic.id.in_(feed["topics"])).all()
                _feed.topics = topics
            db.session.commit()
            return _feed.serialize()
        return jsonify({"message": "Feed could not be updated"}), 500

    @jwt_required()        
    def delete(self, id):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Unauthorized"}, 401
        feed = Feed.query.get(id)
        if feed:
            if feed.user_id != user_id:
                return {"message": "You are not authorized to perform this action"}, 403
            db.session.delete(feed)
            db.session.commit()
            return "", 204
        return jsonify({"message": "Feed could not be deleted"}), 500
    

    
