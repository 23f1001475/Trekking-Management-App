import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False   #tells Flask-SQLAlchemy not to track every modification made to objects : Uses less memory. Improves performance. Removes FSADeprecationWarning warning:

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # to encrypt JWT tokens

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    
    