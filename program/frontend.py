"""Frontend part of the application.

Uses Flask to create a web server and serve websites.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import program.backend

import matplotlib.pyplot as plt
import mpld3

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    """Code to test the ui. Not final."""
    attr = [
        {'name': 'temperature', 'displayName': 'Temperatur'},
        {'name': 'speed', 'displayName': 'Speed'},
        {'name': 'pressure', 'displayName': 'Tryck'},
        {'name': 'downfall', 'displayName': 'Nederbörd'},
        {'name': 'pigs', 'displayName': 'Grisar'},
        {'name': 'sapps', 'displayName': 'Sappar'},
    ]
    data_points = [{
        'id': 1,
        'year': 2020,
        'month': 5,
        'day': 10,
        'time': 12,
        'value': 5,
        'unit': 'celsius'
    }, {
        'id': 2,
        'year': 2020,
        'month': 5,
        'day': 11,
        'time': 12,
        'value': 8,
        'unit': 'celsius'
    }, ]
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4, 5], [3, 1, 4, 1, 5])
    graph = mpld3.fig_to_html(fig)
    return render_template('index.html', attributes=attr, graph=graph)


@bp.route('/upload_historical')
def upload_historical():
    """Code to test the ui. Not final."""
    return render_template('file_upload.html')
