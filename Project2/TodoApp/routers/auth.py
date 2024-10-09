from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users

# {
#   "username": "spiny",
#   "email": "spiny@eed.com",
#   "first_name": "spiny",
#   "last_name": "norman",
#   "password": "paasword",
#   "role": "admin"
# }

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = '00646eac-4362-41e8-a80f-a027b07c71a0'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') # parameter is the url that the client will send to the app


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        
        yield db        # Returns first then continues to close connection.
    finally:
        db.close()


def authenticate_user(username: str, password: str, db):
    user : Users = db.query(Users).filter(Users.username == username).first()    
    if not user:
        return None
    
    if not bcrypt_context.verify(password, user.password_hash):
        return None

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub') # as specified in create_access_token()
        user_id : int = payload.get('id')   # as specified in create_access_token()
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
        
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')        
    
# Dependency injection, calls get_db
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_reqest: CreateUserRequest):
    create_user_model = Users(
        username=create_user_reqest.username,
        email=create_user_reqest.email,
        first_name=create_user_reqest.first_name,
        last_name=create_user_reqest.last_name,
        password_hash=bcrypt_context.hash(create_user_reqest.password),
        role=create_user_reqest.role,
        is_active=True
    )
    
    db.add(create_user_model)
    db.commit()



@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}