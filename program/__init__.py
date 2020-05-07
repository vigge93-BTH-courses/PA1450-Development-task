"""Weather app."""
import os

from flask import Flask


def create_app(test_config=None):
    """Create a flask web application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'weather.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    from . import frontend
    app.register_blueprint(frontend.bp)
    app.add_url_rule('/', endpoint='index')

    return app
