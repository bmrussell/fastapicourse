import pytest
from fastapi import HTTPException, status
from jose import jwt

from ..database import get_db
from ..routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from .utils import *

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    
    user = authenticate_user(test_user.username, 'testpassword', db)    
    assert user is not None
    assert user.username == test_user.username

def test_authenticate_unknown_user(test_user):
    db = TestingSessionLocal()
    
    user = authenticate_user("Unknown", 'testpassword', db)    
    assert user is None

def test_authenticate_wrong_password(test_user):
    db = TestingSessionLocal()
    
    user = authenticate_user(test_user.username, 'wrongpassword', db)    
    assert user is None

def test_authenticate_create_token():
    username = 'spiny'
    id = 1
    role = 'admin'
    token = create_access_token(username, id, role, timedelta(minutes=20))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM,options={'verify_signature': False})
    assert decoded['sub'] == username
    assert decoded['id'] == id
    assert decoded['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_token_valid():
    encode = {'sub': 'spiny', 'id': 1, 'role': 'admin'}    
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    user = await get_current_user(token=token)
    assert user == {'username': 'spiny', 'id': 1, 'user_role': 'admin'}
    
@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as ex:
        await get_current_user(token=token)
    
    assert ex.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert ex.value.detail == 'Invalid user'
