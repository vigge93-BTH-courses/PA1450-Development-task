import flask
from program import create_app

client = None


def setup_module():
    global client
    app = create_app({'TESTING': True, })

    client = app.test_client()


def test_create_app():
    # Given
    test_config1 = None
    test_config2 = {'TESTING': True}

    # When
    app1 = create_app(test_config1)
    app2 = create_app(test_config2)

    # Then
    assert not app1.testing
    assert app2.testing
    assert isinstance(app1, flask.app.Flask)


def test_hello_world():
    # Given
    expected = b'Hello, world!'

    # When
    response = client.get('/hello')

    # Then
    assert response.data == expected
