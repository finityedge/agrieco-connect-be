from . import db, bcrypt
from datetime import datetime, timedelta
from random import choice

# Define the association table for the many-to-many relationship between User and Topic
user_topics = db.Table('user_topics',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)

# Define the association table for the many-to-many relationship between Feed and Topic
feed_topics = db.Table('feed_topics',
    db.Column('feed_id', db.Integer, db.ForeignKey('feeds.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)

feed_likes = db.Table('feed_likes',
    db.Column('feed_id', db.Integer, db.ForeignKey('feeds.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    feeds = db.relationship('Feed', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    role = db.Column(db.String(80), nullable=False, default='user')
    reset_code = db.Column(db.String(32), nullable=True)
    reset_code_expires_at = db.Column(db.DateTime, nullable=True)
    products = db.relationship('Product', backref='user', lazy=True)
    interested_topics = db.relationship('Topic', secondary=user_topics, backref=db.backref('interested_users', lazy=True), lazy=True)
    likes = db.relationship('Feed', secondary=feed_likes, backref=db.backref('liked_by', lazy='dynamic'), overlaps="liked_by,likes")
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, fullname, username, email, password):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password_hash = self.get_hashed_password(password)

    def get_hashed_password(self, password):
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return hash

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def generate_reset_code(self):
        code = ''.join(choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32))
        self.reset_code = code
        self.reset_code_expires_at = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
        return code
    
    def check_reset_code(self, code):
        if self.reset_code == code and self.reset_code_expires_at > datetime.utcnow():
            return True
        return False

    def serialize(self):
        return {
            "id": self.id,
            "fullname": self.fullname if self.fullname else "",
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "interested_topics": [topic.serialize() for topic in self.interested_topics]
        }
    
    def serialize_with_token(self, token):
        return {
            "id": self.id,
            "fullname": self.fullname if self.fullname else "",
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "interested_topics": [topic.serialize() for topic in self.interested_topics],
            "token": token
        }
    
    def serialize_less_sensitive(self):
        return {
            "id": self.id,
            "fullname": self.fullname if self.fullname else "",
            "username": self.username,
            "email": self.email
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    feeds = db.relationship('Feed', secondary=feed_topics, backref=db.backref('feed_topics', lazy=True), lazy=True, overlaps="feed_topics,feeds")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    topics = db.relationship('Topic', secondary=feed_topics, backref=db.backref('topic_feeds', lazy=True), lazy=True, overlaps="feed_topics,feeds")
    comments = db.relationship('Comment', backref='feed', lazy=True)
    likes = db.relationship('User', secondary=feed_likes, backref=db.backref('liked_feeds', lazy='dynamic'), overlaps="liked_by,likes")

    def __repr__(self):
        return f'<Feed {self.id}>'
    
    def __init__(self, content, user_id, images=None):
        self.content = content
        self.user_id = user_id
        self.images = images

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "images": self.images,
            "is_active": self.is_active,
            "topics": [topic.serialize() for topic in self.topics],
            "likes": [user.serialize_less_sensitive() for user in self.likes],
            "comments": [comment.serialize() for comment in self.comments]
        }
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, content, user_id, feed_id):
        self.content = content
        self.user_id = user_id
        self.feed_id = feed_id

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": User.query.get(self.user_id).serialize_less_sensitive(),
            "feed_id": self.feed_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": self.is_active
        }
    
class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, feed_id):
        self.user_id = user_id
        self.feed_id = feed_id

    def serialize(self):
        return {
            "id": self.id,
            "user": User.query.get(self.user_id).serialize_less_sensitive(),
            "feed_id": self.feed_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, price, user_id, description=None, image=None):
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id
        self.image = image

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": self.is_active
        }
    

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.String(80), nullable=False)
    end_time = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    price = db.Column(db.Float, nullable=True)
    image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, title, start_time, end_time, start_date, location, user_id, description=None, price=None, image=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.location = location
        self.price = price
        self.image = image
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.start_date.strftime("%Y-%m-%d"),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "price": self.price,
            "location": self.location,
            "image": self.image,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": self.is_active
        }