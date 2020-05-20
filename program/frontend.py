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

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, DaysTicker, formatters, HoverTool
from bokeh.embed import components
from bokeh.resources import INLINE

import os
import datetime
import calendar
import json

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    """Get datapoints and attributes and display in a graph.

    The arguments are provided through the GET request.

    Args:
        attribute: string with the attribute to filter by.
        timeIntervallType: string with the type of time intervall to filter by.
        timeArgument: list of string(s) containing the time ranges.
    Returns:
        A rendered HTML site with the graph included.
    """
    attributes = backend.get_attributes()
    current_attribute = None
    filters = {}
    if 'attribute' in request.args:
        filters['Argument'] = request.args['attribute']
        for attribute in attributes:
            if request.args['attribute'] == attribute['name']:
                current_attribute = attribute
                break
    if 'timeIntervallType' in request.args and 'timeArgument' in request.args:
        intervallType = request.args['timeIntervallType']
        time_argument = json.loads(request.args['timeArgument'])
        if intervallType == 'months' and len(time_argument[0]) == 2:
            filters['timeIntervallType'] = 'MONTH'
            filters['timeArgument'] = [time_argument, ]
        else:
            filters['timeIntervallType'] = 'TIME_INTERVALL'
            if intervallType == 'year':
                date_start = datetime.datetime(int(time_argument[0]), 1, 1)
                date_end = datetime.datetime(int(time_argument[0]), 12, 31)
            elif intervallType == 'months':
                date = datetime.datetime.strptime(time_argument[0], '%Y-%m')
                date_start = datetime.datetime(date.year, date.month, 1)
                days_in_month = calendar.monthrange(date.year, date.month)[1]
                date_end = datetime.datetime(
                    date.year, date.month, days_in_month)
            else:
                date_start = datetime.datetime.strptime(
                    time_argument[0], '%Y-%m-%d')
                date_end = datetime.datetime.strptime(
                    time_argument[1], '%Y-%m-%d')
            date_start = date_start.strftime('%Y-%m-%d')
            date_end = date_end.strftime('%Y-%m-%d')
            filters['timeArgument'] = [date_start, date_end]
    data_points = backend.get_data(filters)

    if not current_attribute:
        current_attribute = attributes[0]

    for dp in data_points:
        dp['date'] = datetime.datetime(
            dp['year'], dp['month'], dp['day'], dp['time'])

    res = {}
    for dp in data_points:
        for attr in dp:
            if attr in res:
                res[attr].append(dp[attr])
            else:
                res[attr] = [dp[attr]]
    data_points = ColumnDataSource(res)

    p = figure(
        x_axis_label='Time',
        y_axis_label=current_attribute['displayName'],
        x_axis_type='datetime',
        y_range=[min(0, min(data_points.data['value'])-1),
                 max(data_points.data['value'])+1]
    )

    p.xaxis.ticker = DaysTicker(days=list(range(1, 32)))
    p.xaxis.formatter = formatters.DatetimeTickFormatter(days="%Y-%m-%d")

    p.line(x='date', y='value', line_width=2, source=data_points)
    p.circle(x='date', y='value', size=10, source=data_points)

    p.add_tools(
        HoverTool(
            tooltips=[
                ('Datetime', '@date{%Y-%m-%d %H:%M:%S}'),
                ('Value', '@value @unit')
            ],
            formatters={
                '@date': 'datetime'
            },
            mode='vline'
        )
    )

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(p)

    return render_template('index.html',
                           attributes=attributes,
                           selected_attribute=current_attribute,
                           js=js_resources,
                           css=css_resources,
                           script=script,
                           div=div
                           )


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
