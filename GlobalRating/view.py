from flask import *
from GlobalRating import app


@app.route('/')
def index():
    return "Hello, world"