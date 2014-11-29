from flask import render_template
from GlobalRating import app


@app.route('/')
def index():
    items = [
        {
            'name': "First",
            'description': "fdasfdgs"
        },
        {
            'name': "Gogi",
            'description': "Volosatiy nogi"
        }
    ]
    return render_template('index.html', items=items)