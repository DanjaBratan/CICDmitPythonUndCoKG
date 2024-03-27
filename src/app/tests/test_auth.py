from app.models import User, Note
from app import db

# Test successful login with correct credentials
def test_login_success(client):
    # Register a test user first
    user_data = {'email': 'test@example.com', 'firstName': 'TestUserName','password1': 'securepassword', 'password2': 'securepassword'}
    response = client.post('/sign-up', data=user_data)
    assert response.status_code == 302  # Redirect on successful registration

    # Login with registered credentials
    login_data = {'email': 'test@example.com', 'password': 'securepassword'}
    response = client.post('/login', data=login_data)

    # Assert successful login and redirection
    assert response.status_code == 302


# Test login failure with incorrect password
def test_login_fail_wrong_password(client):
    # Register a test user
    user_data = {'email': 'test@example.com', 'firstName': 'TestUserName', 'password1': 'securepassword', 'password2': 'securepassword'}
    response = client.post('/sign-up', data=user_data)
    assert response.status_code == 302  # Redirect on successful registration

    # Login with incorrect password
    login_data = {'email': 'test@example.com', 'password': 'wrongpassword'}
    response = client.post('/login', data=login_data)

    # Assert failed login and presence of error message
    assert response.status_code == 200
    assert b'Falsches Passwort!' in response.data  # Assuming error message is in German
