from GlobalRating import db
from GlobalRating.models import Category, Rating, User


def get_all(type):
    query = db.session.query(Category).filter(Category.type == type)
    return query.all()


def get_category(id):
    query = Category.query.get(id)
    return query


def get_user(id):
    return User.query.get(id)


def get_all_children(id):
    query = db.session.query(Category).filter(Category.parent_id == id)
    return query.all()


def get_mark_and_voices(id):
    query = db.session.query(Rating).filter(Rating.cat_id == id)

    mas = query.all()
    sum_mas = 0
    for mark in mas:
        sum_mas += mark.mark

    if len(mas) == 1:
        number_of_elements = 1
    else:
        number_of_elements = len(mas) - 1

    return int(round(sum_mas / number_of_elements)), len(mas) - 1


def rate_category(id_user, id_cat, rating):
    user = get_user(id_user)
    category = get_category(id_cat)
    rating = Rating(mark=rating, category=category, author=user)
    db.session.add(rating)
    db.session.commit()


def add_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()


def add_category(name, description, type, parent="root", address="lool",
                 url="http://cs411222.vk.me/v411222468/2129/DudmSflxmSQ.jpg"):
    cat = Category(name=name, description=description, type=type,
                   parent_id=parent, address=address, url=url)
    rating = Rating(mark=0, category=cat)
    db.session.add(cat)
    db.session.add(rating)
    db.session.commit()

