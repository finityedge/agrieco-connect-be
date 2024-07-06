from . import db, bcrypt
from datetime import datetime

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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    feeds = db.relationship('Feed', backref='user', lazy=True)
    interested_topics = db.relationship('Topic', secondary=user_topics, backref=db.backref('interested_users', lazy=True), lazy=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "interested_topics": [topic.serialize() for topic in self.interested_topics]
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    feeds = db.relationship('Feed', secondary=feed_topics, backref=db.backref('feed_topics', lazy=True), lazy=True)

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
    topics = db.relationship('Topic', secondary=feed_topics, backref=db.backref('topic_feeds', lazy=True), lazy=True)

    def __repr__(self):
        return f'<Feed {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "images": self.images,
            "is_active": self.is_active,
            "topics": [topic.serialize() for topic in self.topics]
        }
