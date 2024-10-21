from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Users
from .auth import bcrypt_context, get_current_user

router = APIRouter()
router = APIRouter(prefix='/users', tags=['users'])



# Dependency injection, calls get_db & get_current_user
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class UserProfile():
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    is_active: bool

class UpdateUserRequest(BaseModel):
    username: str = Field(None, min_length=3)
    email: str = Field(None, min_length=3)
    first_name: str = Field(None, min_length=3)
    last_name: str = Field(None, min_length=3)
    old_password: str = Field(None, min_length=3)
    password: str = Field(None, min_length=3)
    role: str = Field(None, min_length=3)
    phone_number: str = Field(None, min_length=3)
    is_active: bool = Field(None)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: user_dependency, db: db_dependency, create_user_reqest: CreateUserRequest):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not authenticated.')

    create_user_model = Users(
        username=create_user_reqest.username,
        email=create_user_reqest.email,
        first_name=create_user_reqest.first_name,
        last_name=create_user_reqest.last_name,
        password_hash=bcrypt_context.hash(create_user_reqest.password),
        role=create_user_reqest.role,
        phone_number=create_user_reqest.phone_number,
        is_active=True
    )
    
    db.add(create_user_model)
    db.commit()
    
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_profile(user: user_dependency,  db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated.')

    user_model = db.query(Users)\
        .filter(Users.id == user.get('id'))\
        .first()    

    profile_model = db.query(Users)\
        .filter(Users.id == user_id)\
        .first()    

    
    if user_model.id != profile_model.id and user_model.role != 'admin':
        raise HTTPException(status_code=400, detail='Regular users can only get own profile.')
    
    
    
    profile = UserProfile()
    profile.id = profile_model.id
    profile.first_name = profile_model.first_name
    profile.last_name = profile_model.last_name
    profile.role = profile_model.role
    profile.phone_number = profile_model.phone_number
    profile.email = profile_model.email
    profile.is_active = profile_model.is_active
    
    return profile


class PasswordChangeRequest(BaseModel):
    old_password: str = Field(None, min_length=3)
    new_password: str = Field(..., min_length=3)
    
@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency, db: db_dependency, updated_user: UpdateUserRequest, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated.')

    user_model = db.query(Users)\
        .filter(Users.id == user.get('id'))\
        .first() 
    
    if user_model.role != "admin" and user_model != user_id:
        raise HTTPException(status_code=400, detail='Only admins can update other users.')
        
    if updated_user.password is not None:
        if (user_model.role != "admin" and (updated_user.old_password is None or updated_user.old_password == "" or updated_user.password == "") ):
            raise HTTPException(status_code=400, detail='Must supply old and new password.')
    
        if user_model.role != "admin":
            if not bcrypt_context.verify(updated_user.old_password, user_model.password_hash):
                raise HTTPException(status_code=400, detail='Old password does not match.')
        
        user_model.password_hash = bcrypt_context.hash(updated_user.password)

    if updated_user.first_name is not None: user_model.first_name = updated_user.first_name
    if updated_user.last_name is not None: user_model.last_name = updated_user.last_name
    if updated_user.email is not None: user_model.email = updated_user.email
    if updated_user.phone_number is not None: user_model.phone_number = updated_user.phone_number
    
    if user_model.role != "admin":
        if updated_user.role is not None or updated_user.is_active is not None:
            raise HTTPException(status_code=400, detail='Only admin can update role and active status.')
    
    if updated_user.role is not None: user_model.role = updated_user.role
    if updated_user.is_active is not None: user_model.role = updated_user.is_active
    
    db.add(user_model)
    db.commit()
