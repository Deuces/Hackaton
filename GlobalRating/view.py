import codecs

from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from GlobalRating import app, oid, lm
from GlobalRating.dbAPI import *
from GlobalRating.forms import RatingForm, AddForm
from GlobalRating.models import ROLE_USER
from config import OPENID_PROVIDERS


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
def start():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('start.html')


@app.route('/try_auth/<social>', methods=['GET', 'POST'])
@oid.loginhandler
def try_auth(social):
    if request.method == 'GET':
        return oid.try_login(OPENID_PROVIDERS[int(social)].get('url'), ask_for=['nickname', 'email'])
    else:
        return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('start'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(name=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/index')
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


@app.route('/info')
def show_info():
    f = codecs.open('/GlobalRating/static/js/data.tsv', "w", "utf-8")
    categories = get_all('university')
    for i in categories:
        mark, voices = get_mark_and_voices(i.id)
        f.write(i.name + "\t" + str(mark) + "\n")
    g.close
    return render_template('infograph.html')


@app.route('/item/<item_id>', methods=['GET', 'POST'])
def show_item(item_id):
    form = RatingForm()
    if request.method == 'POST':
        rate_category(int(g.user.get_id()), item_id, int(form.rating.data))
        return redirect(url_for('index'))
    else:
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

        votable = True
        if g.user.is_authenticated():
            query = db.session.query(Rating).filter(Rating.usr_id == int(g.user.get_id())).filter(
                Rating.cat_id == item_id).first()
            if query is not None:
                votable = False
    return render_template('item.html', item=item, children=children, votes=votes, stars=stars, votable=votable,
                           form=form)


@app.route('/add/<id>', methods=['POST', 'GET'])
@login_required
def add_child(id):
    form = AddForm()
    if request.method == 'POST':
        address = ''.join(form.address.data.split())
        add_category(form.name.data, form.type.data, parent=id, description=form.description.data, url=form.url.data,
                     address=address)
        return redirect(url_for('index'))
    return render_template('add.html', id=id, form=form)


@app.route('/about.html')
def about():
    return render_template('about.html')