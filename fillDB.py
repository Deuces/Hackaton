from GlobalRating import db
from GlobalRating.dbAPI import *
from GlobalRating.models import User, Rating, Category

add_category("NTUU", "Very cool university", "university")
add_category("NAU", "Very low university", "university")
add_category("KNUTD", "Not Very cool university", "university")

add_user("Gogli", "dfdsadg")
rate_category(1, 2, 5)


cat = get_category(1)
add_category("IASA", "Not cool faculty", "faculty", parent=cat.id)