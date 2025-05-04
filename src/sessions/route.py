from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from src.dtos.session_dto import Token, User, UserListResponse, UserListItem
from src.infra.database import get_db
from src.sessions.create_token import create_access_token
from src.sessions.create_user import create_user
from src.sessions.find_user import find_user
from src.sessions.list_users import list_users
from src.sessions.password_hash import verify_password

sessions_router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
    responses={201: {"description": "User created successfully"},
               401: {"description": "Invalid credentials"},
               409: {"description": "User already exists"},
               500: {"description": "Internal server error"}}
)


@sessions_router.post("/", summary="Add new user")
async def add_user(user: User, db: Session = Depends(get_db)):
    user_created = create_user(user, db)
    if not user_created:
        return JSONResponse(status_code=409, content={'message': f'User {user.email} already exists'})
    return JSONResponse(status_code=201, content={})


@sessions_router.post("/token", summary="Login operation")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_db = find_user(db, form_data.username)
    if user_db is None or not verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({'sub': user_db.email})
    return Token(access_token=access_token,
                 token_type="bearer")


@sessions_router.post("/api-token",  summary="Login operation with token")
async def login_api(user: User, db: Session = Depends(get_db)):
    user_db = find_user(db, user.email)
    if user_db is None or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({'sub': user_db.email})
    return Token(access_token=access_token,
                 token_type="bearer")


@sessions_router.get("/users", response_model=UserListResponse, summary="List all users")
async def get_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all registered users in the system.
    
    This endpoint returns a list of users with only their ID and email address.
    No sensitive information like passwords is included in the response.
    
    Returns:
        A list of users with their ID and email, along with the total count.
    """
    users, total = list_users(db)
    
    # Convert to DTO objects, including only id and email
    user_items = [UserListItem(id=user.id, email=user.email) for user in users]
    
    return UserListResponse(
        users=user_items,
        total=total
    )
