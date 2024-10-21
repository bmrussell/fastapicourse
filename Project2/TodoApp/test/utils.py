from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context, create_access_token

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
    return {'id': 1,
            'first_name': "spiny",
            'last_name': "norman",
            'role': "admin",
            'phone_number': "0118 999 881 999 119 725 3",
            'email': "spiny@eed.com",
            'is_active': True}


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


@pytest.fixture
def test_user():
    
    # Make sure DB is clean of test users
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create a test user
    hash = bcrypt_context.hash("testpassword")
    user = Users(
        id=1,
        email="spiny@eed.com",
        username="spiny",
        first_name="spiny",
        last_name="norman",
        password_hash=hash,
        is_active=True,
        role="admin",
        phone_number="0118 999 881 999 119 725 3"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    
    # Authenticate the test user
    token = create_access_token("spiny", 1, "admin", timedelta(minutes=20))
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    # Yield returns todo to the calling test
    yield user
    # When the calling test terminates the rest is executed

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
