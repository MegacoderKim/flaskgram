import json
import pytest
from dotenv import load_dotenv

from socio.models import User
from socio.app import create_app
from socio.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory, PostFactory, CommentFactory


register(UserFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def auth_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin',
        first_name="admin",
        last_name="flaskadmin"
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def anonymous_headers(client):
    return {
        'content-type': 'application/json'
    }


@pytest.fixture
def user_headers(auth_user, client):
    data = {
        'username': auth_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def user_refresh_headers(auth_user, client):
    data = {
        'username': auth_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
