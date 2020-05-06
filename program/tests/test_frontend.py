import flask
from program import create_app

client = None


def setup_module():
    global client
    app = create_app({'TESTING': True, })

    client = app.test_client()


def test_index():
    response = client.get('/')
    assert response.data == b'Hello, world!'
