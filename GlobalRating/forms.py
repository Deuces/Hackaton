import flask.ext.wtf
from wtforms import RadioField


class RatingForm(flask.ext.wtf.Form):
    rating = RadioField('rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])