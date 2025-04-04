from sqlalchemy.orm import Session
from src.models.user import User as Entity


def find_user(db: Session, email: str):
    user = db.query(Entity).filter(Entity.email == email).one_or_none()
    if user is None:
        return None
    return user