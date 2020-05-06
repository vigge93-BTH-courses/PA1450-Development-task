"""Frontend part of the application.

Uses Flask to create a web server and serve websites.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import program.backend

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    """Hello world."""
    return 'Hello, world!'
