import sys
from . import db
import os

from flask import Flask, g, render_template, redirect, url_for, request, flash
from flask.helpers import url_for
from werkzeug.utils import secure_filename

import logging

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE = os.path.join(app.instance_path, 'src.sqlite'),
		UPLOAD_FOLDER = os.path.join(app.instance_path, 'artwork')
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	


	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import page
	app.register_blueprint(page.bp)

	@app.route('/')
	def root():
		return redirect(url_for('auth.signin'))

	

	@app.route('/hello')
	def hello():
		print('hello')
		sys.stdout.flush()
		return 'hello world'

	return app

