import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's)m3R@nd0mC0d3!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFIX = '/api'
    UPLOAD_FOLDER = 'app/static/uploads'
    