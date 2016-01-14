import pytest

import os
import rPi
import tempfile
import pytest

@pytest.fixture
def client(request):
    db_fd, rPi.app.config['DATABASE'] = tempfile.mkstemp()
    client = rPi.app.test_client()
    with rPi.app.app_context():
        rPi.init_db()

    def teardown():
        """Get rid of the database again after each test."""
        os.close(db_fd)
        os.unlink(rPi.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client


def register(client, username, password, password2=None, email=None):
    """Helper function to register a user"""
    if password2 is None:
        password2 = password
    if email is None:
        email = username + '@example.com'
    return client.post('/register', data={
        'username':     username,
        'password':     password,
        'password2':    password2,
        'email':        email,
    }, follow_redirects=True)


def login(client, username, password):
    """Helper function to login"""
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)


def register_and_login(client, username, password):
    """Registers and logs in in one go"""
    register(client, username, password)
    return login(client, username, password)


def logout(client):
    """Helper function to logout"""
    return client.get('/logout', follow_redirects=True)


def test_register(client):
    """Make sure registering works"""
    rv = register(client, 'user1', 'default')
    assert b'You were successfully registered ' \
           b'and can login now' in rv.data
    rv = register(client, 'user1', 'default')
    assert b'The username is already taken' in rv.data
    rv = register(client, '', 'default')
    assert b'You have to enter a username' in rv.data
    rv = register(client, 'meh', '')
    assert b'You have to enter a password' in rv.data
    rv = register(client, 'meh', 'x', 'y')
    assert b'The two passwords do not match' in rv.data
    rv = register(client, 'meh', 'foo', email='broken')
    assert b'You have to enter a valid email address' in rv.data


def test_login_logout(client):
    """Make sure logging in and logging out works"""
    rv = register_and_login(client, 'user1', 'default')
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, 'user1', 'wrongpassword')
    assert b'Invalid password' in rv.data
    rv = login(client, 'user2', 'wrongpassword')
    assert b'Invalid username' in rv.data
