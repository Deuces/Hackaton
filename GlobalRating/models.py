from GlobalRating import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, index=True)
    usr_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    type = db.Column(db.String(64), index=True)
    parent_id = db.Column(db.Integer, index=True, nullable=True)
    address = db.Column(db.String(64), index=True, nullable=True)
    url = db.Column(db.String(128), index=True, nullable=True)
    ratings = db.relationship('Rating', backref='category', lazy='dynamic')