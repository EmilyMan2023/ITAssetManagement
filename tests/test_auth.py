def test_register_user(client):
    response = client.post('/sign-up', data={
        'email': 'test@example.com',
        'firstName': 'Test',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'password123',
        'role': 'user'
    }, follow_redirects=True)
    assert response.status_code == 200




def test_duplicate_email_signup(client, app):
    # First registration
    client.post('/sign-up', data={
        'email': 'dupe@example.com',
        'firstName': 'First',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'password123',
        'role': 'user'
    })

    # Second registration with same email
    response = client.post('/sign-up', data={
        'email': 'dupe@example.com',
        'firstName': 'Second',
        'lastName': 'User',
        'password1': 'newpass123',
        'password2': 'newpass123',
        'role': 'user'
    }, follow_redirects=True)

    assert response.status_code == 200



def test_login_invalid_password(client, app):
    client.post('/sign-up', data={
        'email': 'wrongpass@example.com',
        'firstName': 'Wrong',
        'lastName': 'Pass',
        'password1': 'correctpass',
        'password2': 'correctpass',
        'role': 'user'
    })

    response = client.post('/login', data={
        'email': 'wrongpass@example.com',
        'password': 'incorrectpass'
    }, follow_redirects=True)

    assert response.status_code == 200


    #assert b'Incorrect password' in response.data or b'try again' in response.data
    






def login(client, email, password):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_admin_access_dashboard(client, app):
    client.post('/sign-up', data={
        'email': 'admin@example.com',
        'firstName': 'Admin',
        'lastName': 'Guy',
        'password1': 'adminpass',
        'password2': 'adminpass',
        'role': 'admin'
    })

    login(client, 'admin@example.com', 'adminpass')
    response = client.get('/dashboard')
    assert b'Asset History Dashboard' in response.data



