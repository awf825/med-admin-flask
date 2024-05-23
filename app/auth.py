import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import Users

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            # try:
            user = Users(
                email=request.form["email"],
                password=generate_password_hash(request.form["password"]),
                auth_method_id=1
            )
            db.session.add(user)
            db.session.commit()
            # except db.IntegrityError:
            #     error = f"User {email} is already registered."
        else:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        stmt = db.select(Users).where(Users.email == email)
        result = db.session.execute(stmt)
        user = None
        for user_obj in result.scalars():
            user = user_obj

        if not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')

# bp.before_app_request() registers a function that runs before the view function, 
# no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        stmt = db.select(Users).where(Users.user_id == user_id)
        result = db.session.execute(stmt)
        user = None
        for user_obj in result.scalars():
            user = user_obj
        g.user = user

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Creating, editing, and deleting blog posts will require a user to be logged in. 
# A decorator can be used to check this for each view it’s applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view