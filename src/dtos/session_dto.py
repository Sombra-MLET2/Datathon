from pydantic import BaseModel, Field, EmailStr, PositiveInt
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: PositiveInt | None = Field(None, gt=0)
    email: EmailStr | None = None
    password: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = True


class TokenData(BaseModel):
    email: str


class UserListItem(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserListItem]
    total: int
