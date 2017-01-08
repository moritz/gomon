from gomon.model import read_data
from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    model = read_data()
    return render_template('index.html',
                unreleased=model.unreleased)
