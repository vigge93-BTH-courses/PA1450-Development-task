import flask
from program import create_app

client = None


def setup_module():
    global client
    app = create_app({'TESTING': True, })

    client = app.test_client()


def test_index():
    # Given
    expected = b'Hello, world!'
    path = '/'

    # When
    response = client.get(path)

    # Then
    assert response.data == expected
