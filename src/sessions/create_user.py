from sqlalchemy.orm import Session
from src.models.user import User as Entity
from src.dtos.session_dto import User as DTO
from src.sessions.password_hash import bcrypt_password


def create_user(user: DTO, db: Session) -> bool:
    exists = db.query(Entity).filter(Entity.email == user.email).one_or_none()
    if exists is not None:
        return False
    new_user = Entity(email=user.email, hashed_password=bcrypt_password(user.password), is_active=True)
    db.add(new_user)
    db.commit()
    return True