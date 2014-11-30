from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from GlobalRating import app, oid, lm
from GlobalRating.dbAPI import *
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
    return render_template('infograph.html')


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