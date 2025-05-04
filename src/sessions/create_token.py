from datetime import timedelta, datetime, timezone
import jwt
from src.infra import configs as data_config


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=data_config.JWT_EXPIRY)
    to_encode =  data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, data_config.JWT_SECRET, algorithm=data_config.JWT_ALGORITHM)