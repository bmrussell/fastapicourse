from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

from ..database import Base
from ..main import app
from ..routers.auth import get_current_user
from ..routers.todos import get_current_user, get_db

SQLALCHEMY_DATABSE_URL = 'sqlite:///./todos-test.db'

engine = create_engine(
        SQLALCHEMY_DATABSE_URL, connect_args={'check_same_thread': False},
        poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

#Base = declarative_base() 


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'spiny', 'id': 1, 'user_role': 'admin', 'phone_number': ''}

# Change the dependency injection to use the database and user from this module
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_read_all_authenticated():
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []