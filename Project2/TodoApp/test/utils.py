import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..models import Todos

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