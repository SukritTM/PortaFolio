import functools
from flask import current_app, g, flash, get_flashed_messages, Blueprint, redirect, render_template, request, session, url_for, abort

from werkzeug.security import generate_password_hash as hash, check_password_hash as checkhash

from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
	if request.method == 'POST':
		name = request.form['name']
		username = request.form['user-name']
		email = request.form['email']
		password = request.form['pw']
		dob = request.form['dob']
		prepeat = request.form['repeat-pw']

		if not (name and username and email and password and prepeat):
			abort(400)
		
		db = get_db()
		try:
			db.execute(
				"insert into user (name, username, email, password, dob) values (?, ?, ?, ?, ?)",
				(name, username, email, hash(password), dob)
			)
			db.commit()
		except db.IntegrityError:
			flash('Username or Email is taken')
		else:
			return redirect(url_for('auth.signin'))
	
	return render_template('signup.html')

@bp.route('/signin', methods=('GET', 'POST'))
def signin():
	if request.method == 'POST':
		identity = request.form['user-name']
		password = request.form['pw']

		if is_email(identity):
			query = 'email'
		else:
			query = 'username'
		
		db = get_db()

		user = db.execute(
			f'select * from user where {query} = ?', (identity, )
		).fetchone()

		error = None
		if not user:
			error = 'No such user exists'
		elif not checkhash(user['password'], password):
			error = 'Incorrect password'
		
		if not error:
			session.clear()
			session['user_id'] = user['uid']
			return redirect(url_for('showuser'))
		
		flash(error)
	
	return render_template('signin.html')

@bp.route('/signout')
def signout():
	session.clear()
	return redirect(url_for('auth.signin'))

@bp.before_app_request
def load_user_session():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
            'SELECT * FROM user WHERE uid = ?', (user_id,)
        ).fetchone()

def is_email(value: str):
	if '@' in value:
		return True
	return False

def login_required(view):
	@functools.wraps(view)
	def wrapper(*args, **kwargs):
		if g.user is None:
			return redirect(url_for('auth.signin'))
		
		return view(*args, **kwargs)
	
	return wrapper

