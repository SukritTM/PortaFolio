from . import db
import os

from flask import Flask, g, render_template
from flask.helpers import url_for


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE = os.path.join(app.instance_path, 'src.sqlite')
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

	@app.route('/showuser')
	@auth.login_required
	def showuser():
		user = g.user
		return render_template('index.html')

	@app.route('/hello')
	def hello():
		return 'hello world'

	return app

