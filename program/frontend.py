"""Frontend part of the application.

Uses Flask to create a web server and serve websites.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    current_app
)
from werkzeug.utils import secure_filename

import program.backend as backend

import matplotlib.pyplot as plt
import mpld3

import os


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


@bp.route('/upload_historical', methods=('GET', 'POST'))
def upload_historical():
    """Render the upload file webpage and handle uploaded file.

    Render file_upload.html if method is GET.

    Save file to file system, call backend to process data
    and render index.html if method is POST.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.instance_path, filename))
            message = backend.process_file(filename)
            flash(message)
            return redirect(url_for('index'))
        else:
            flash("Invalid file type")

    return render_template('file_upload.html')


def allowed_file(filename):
    """Test if filename is allowed.

    Args:
        filename: string with the name of the file.
    Returns:
        True if filename is allowed, otherwise False.
    """
    ALLOWED_EXTENSIONS = ('csv')
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
