import os


ENV = os.getenv('MUSH_ENV') if os.getenv('MUSH_ENV') else 'dev'
SQLALCHEMY_DATABASE_URL = os.getenv('MUSH_DATABASE_URL') if os.getenv('MUSH_DATABASE_URL') else "sqlite:///./datathon.db"
JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET') if os.getenv('JWT_SECRET') else '8e8e092f6c6d48839b5b514b3edb7d58'
JWT_EXPIRY = os.getenv('JWT_EXPIRY') if os.getenv('JWT_EXPIRY') else 30