import pytest

from admin.views import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_login_admin(client):
    response = client.get('/login_admin')
    assert response.status_code == 200


def test_failed_login(client):
    response = client.post('/login_admin', data={
        'username': 'wrong_user',
        'password': 'wrong_password'
    })

    assert response.status_code == 200


def test_redirect_to_login(client):
    response = client.get('/admin/')
    assert response.status_code == 302
    assert 'login_admin' in response.location


def test_admin_index_access(client):
    client.post('/login_admin', data={
        'username': 'admin',
        'password': 'password'
    })

    response = client.get('/admin/')
    assert response.status_code == 302
