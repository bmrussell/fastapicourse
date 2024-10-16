import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

from ..database import Base
from ..main import app
from ..models import Todos
from ..routers.auth import get_current_user
from ..routers.todos import get_current_user, get_db

SQLALCHEMY_DATABSE_URL = 'sqlite:///./todos-test.db'

engine = create_engine(
    SQLALCHEMY_DATABSE_URL, connect_args={'check_same_thread': False},
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


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


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Learn every day",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    
    # Yield returns todo to the calling test
    yield todo
    # When the calling test terminates the rest is executed
    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'priority': 5, 'id': 1, 'complete': False, 'description': 'Learn every day', 'title': 'Learn to code', 'owner_id': 1}]
