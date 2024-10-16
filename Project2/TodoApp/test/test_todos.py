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


def test_read_all_authenticated(test_todo: Todos):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'priority': 5, 'id': 1, 'complete': False, 'description': 'Learn every day', 'title': 'Learn to code', 'owner_id': 1}]

def test_read_one_authenticated(test_todo: Todos):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'priority': 5, 'id': 1, 'complete': False, 'description': 'Learn every day', 'title': 'Learn to code', 'owner_id': 1}

def test_read_one_not_found_authenticated(test_todo: Todos):
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}

def test_create_authenticated(test_todo: Todos):
    request_data = {
        'title': 'New Todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False
    }
    response = client.post('/todos', json=request_data)    
    assert response.status_code == 201
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
def test_update_authenticated(test_todo: Todos):
    request_data = {
        'title': 'Updated title',
        'description': 'Updated description',
        'priority': 5,
        'complete': False
    }
    response = client.put('/todos/1', json=request_data)    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
def test_update_not_found_authenticated(test_todo: Todos):
    request_data = {
        'title': 'Updated title',
        'description': 'Updated description',
        'priority': 5,
        'complete': False
    }
    response = client.put('/todos/999', json=request_data)    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Todo not found.'}
    
    
def test_delete_authenticated(test_todo: Todos):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_not_found_authenticated(test_todo: Todos):
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Todo not found.'}
