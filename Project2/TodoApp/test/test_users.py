from fastapi import status

from ..database import get_db
from .utils import *

# Change the dependency injection to use the database and user from this module
app.dependency_overrides[get_db] = override_get_db
#app.dependency_overrides[get_current_user] = override_get_current_user

def test_users_return_user(test_user):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    
    assert response.json() == {'id': 1, 'first_name': 'spiny', 'last_name': 'norman', 'role': 'admin', 'phone_number': '0118 999 881 999 119 725 3', 'email': 'spiny@eed.com', 'is_active': True}

def test_users_change_password_success(test_user):
    response = client.put("/users/1", json={"old_password": "testpassword", "password": "loveleyjubbly"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_users_change_password_fail(test_user):
    # Test changing password supplying old one
    response = client.put("/users/1", json={"old_password": "wrongpassword", "password": "loveleyjubbly"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_users_change_password_admin(test_user):
    # Test admin changing password without supplying old one
    response = client.put("/users/1", json={"password": "loveleyjubbly"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_users_change_phone_success(test_user):
    # Test admin changing password without supplying old one
    response = client.put("/users/1", json={"phone_number": "000"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
