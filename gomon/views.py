from gomon.config import config
from gomon.model import read_data
from gomon import app
from flask import render_template, send_from_directory

@app.route('/')
@app.route('/index')
def index():
    model = read_data()
    return render_template('index.html',
                last_updated=model.last_updated,
                unreleased=model.unreleased[:8],
                failed=model.failed[:8],
                paused=model.paused[:8],
                base_url=config()['goserver']['url'],
    )
