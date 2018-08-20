"""
test_login_logout.py is a functional test suite with an obvious purpose.
mwroffo August 2018
"""

def test_login_redirect(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested via GET
    THEN check that the response is a 302 redirect to /login
    """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data

def test_login_200(test_client):
    """
    GIVEN a Flask app
    WHEN the '/login' page is requested directly via GET
    THEN check that the response is 200
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_valid_login_logout(test_client, init_db):
    """
    GIVEN a Flask app
    WHEN a client submit a login request via POST
    THEN check that the response is valid
    """
    response = test_client.post('/login',
        data=dict(username='mroffo', password='password', remember_me=False),
        follow_redirects=True)
    assert b"Welcome, mroffo, to FastCards" in response.data
    assert b'New user?' not in response.data
    '''
    WHEN client submits post request to /logout
    THEN check that the user was logged out.
    '''
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, mroffo, to FastCards" not in response.data
    assert b'New user?' in response.data