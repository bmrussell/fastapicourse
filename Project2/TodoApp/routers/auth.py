from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models import Users

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = '00646eac-4362-41e8-a80f-a027b07c71a0'
ALGORITHM = 'HS256'

# pip install bcrypt==4.0.1
# version of bcrypt important 
# for  pip install "python-jose[cryptography]"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') # parameter is the url that the client will send to the app

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user : Users = db.query(Users).filter(Users.username == username).first()    
    if not user:
        return None
    
    if not bcrypt_context.verify(password, user.password_hash):
        return None

    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


    
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')     # as specified in create_access_token()
        user_id : int = payload.get('id')       # as specified in create_access_token()
        user_role : int = payload.get('role')   # as specified in create_access_token()
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')        
    
# Dependency injection, calls get_db
db_dependency = Annotated[Session, Depends(get_db)]


templates = Jinja2Templates(directory="TodoApp/templates")

### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### API ###

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}