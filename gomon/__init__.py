from flask import Flask

app = Flask(__name__)
from gomon import views
