from fastapi import status

from ..database import get_db
from ..models import Users
from ..routers.auth import create_access_token, get_current_user
from .utils import *

# Change the dependency injection to use the database and user from this module
app.dependency_overrides[get_db] = override_get_db
#app.dependency_overrides[get_current_user] = override_get_current_user

def test_users_return_user(test_user):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    
    assert response.json() == {'id': 1, 'first_name': 'spiny', 'last_name': 'norman', 'role': 'admin', 'phone_number': '0118 999 881 999 119 725 3', 'email': 'spiny@eed.com', 'is_active': True}
