import logging
import os

logger = logging.getLogger("uvicorn")

# Standard configuration
ENV = os.getenv('ENV') if os.getenv('ENV') else 'dev'
SQLALCHEMY_DATABASE_URL = "sqlite:///./datathon.db"
JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET') if os.getenv('JWT_SECRET') else '8e8e092f6c6d48839b5b514b3edb7d58'
JWT_EXPIRY = os.getenv('JWT_EXPIRY') if os.getenv('JWT_EXPIRY') else 30
# ML_MODEL_NAME = "RandomForest"
ML_MODEL_NAME = "XGBoost"

# Ollama configuration
OLLAMA_HOST = "192.168.50.140:11434" # 4080S
OLLAMA_MODEL = "mistral:latest"
OLLAMA_REQUEST_TIMEOUT = 180