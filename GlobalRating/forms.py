import flask.ext.wtf
from wtforms import RadioField, Form, TextField
from wtforms.validators import Required


class RatingForm(flask.ext.wtf.Form):
    rating = RadioField('rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])


class AddForm(flask.ext.wtf.Form):
    name = TextField('Name', validators=[Required()])
    type = TextField('Type', validators=[Required()])
    description = TextField('Description', validators=[Required()])
    url = TextField('Image', validators=[Required()])
    address = TextField('Address', validators=[Required()])
