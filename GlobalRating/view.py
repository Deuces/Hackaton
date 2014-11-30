from flask import render_template
from GlobalRating import app
from GlobalRating.dbAPI import *


@app.route('/index.html')
def index():
    categories = get_all("university")
    items = []
    for i in categories:
        stars, votes = get_mark_and_voices(i.id)
        items.append({
            "category": i,
            "stars": stars,
            "votes": votes
        })
    return render_template('index.html', items=items)


@app.route('/item/<item_id>')
def show_item(item_id):
    item = get_category(item_id)
    children_cat = get_all_children(item_id)
    children = []
    for i in children_cat:
        stars, votes = get_mark_and_voices(i.id)
        children.append({
            "category": i,
            "stars": stars,
            "votes": votes
        })
    stars, votes = get_mark_and_voices(item_id)
    return render_template('item.html', item=item, children=children, votes=votes, stars=stars)

@app.route('/')
def start():
    return render_template('start.html')