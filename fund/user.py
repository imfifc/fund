from flask import Blueprint, request, session, redirect, url_for, render_template
from fund.dbs import db
from fund.models import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    return '用户首页'


@bp.route('/profile')
def profile():
    return '个人首页'


@bp.route('/reg')
def register():
    pass


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        print(111, dir(session))
        # 1, 首先检查session，判断用户是否第一次登录，如果不是，则直接重定向到首页
        if 'username' in session:
            return redirect('/show')
        if 'username' in request.cookies:
            session['username'] = request.cookies['username']
            return redirect(url_for('/show'))
        return render_template('user/login.html')
    if request.method == "POST":
        form = request.form.to_dict()
        username = form.get('username')
        password = form.get('password')
        data = {
            'username': form.get('username'),
            'password': form.get('password')
        }
        u = User(**data)
        db.session.add(u)
        db.session.commit()
        return 'add user success'


@bp.route('/logout')
def logout():
    pass
