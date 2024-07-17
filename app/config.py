import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's)m3R@nd0mC0d3!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFIX = '/api'
    UPLOAD_FOLDER = 'app/static/uploads'
<<<<<<< HEAD
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'sk-proj-wxPVT91fhdm62sqn6HwxT3BlbkFJ0WZJhrqshrR9ZyeVyd3J'
=======
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
>>>>>>> b1b52961c068a4e76ca27ed8e8ee85a419899456
    