import flask
from program import create_app

client = None


def setup_module():
    global client
    app = create_app({'TESTING': True, })

    client = app.test_client()


def test_create_app():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    assert isinstance(create_app(), flask.app.Flask)


def test_hello_world():
    response = client.get('/hello')
    assert response.data == b'Hello, world!'
