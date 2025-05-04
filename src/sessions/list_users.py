from sqlalchemy.orm import Session
from typing import List, Tuple
from src.models.user import User as Entity


def list_users(db: Session) -> Tuple[List[Entity], int]:
    """
    Retrieve all users from the database
    
    Args:
        db: Database session
        
    Returns:
        Tuple containing a list of user entities and the total count
    """
    users = db.query(Entity).all()
    total = len(users)
    return users, total
