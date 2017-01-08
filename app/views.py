from gomon.config import config
from gomon.model import read_data
from app import app
from flask import render_template, send_from_directory

@app.route('/')
@app.route('/index')
def index():
    model = read_data()
    return render_template('index.html',
                unreleased=model.unreleased[:8],
                failed=model.failed[:8],
                base_url=config()['goserver']['url'],
    )

#@app.route('/static/<path:path>')
#def handle_static(path):
#    return send_from_directory('static', path)
