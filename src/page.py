from flask import current_app, g, flash, get_flashed_messages, Blueprint, redirect, render_template, request, session, url_for, abort, send_file
from src.db import get_db
from src.auth import login_required
import os

bp = Blueprint('page', __name__, url_prefix='')

@bp.route('/home', methods=('GET', 'POST'))
@login_required
def home():
	user = g.user
	
	db = get_db()
	if request.method == 'POST':

		if 'art' not in request.files:
			flash("No file part uploaded")
			return render_template('editor.html', name=g.user['name'])
		
		files = request.files.getlist('art')
		
		for file in files:
			fname = getfilename()
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fname))

			db.execute(
				"INSERT INTO artwork (image, uid) VALUES (?, ?)",
				(fname, user['uid'])
			)
			db.commit()

	fnames = db.execute(
		"""
		SELECT image FROM
		artwork INNER JOIN user
		ON artwork.uid == user.uid
		"""
	).fetchall()

	fnames = [fname['image'] for fname in fnames]
	

	flash(fnames)

	return render_template('editor.html', name=g.user['name'], fnames=fnames)

@bp.route('/img/<fname>')
def image(fname: str):
	path = os.path.join(current_app.config['UPLOAD_FOLDER'], fname)
	return send_file(path, mimetype='image')



def getfilename():
	lis = os.listdir(current_app.config['UPLOAD_FOLDER'])
	return 'img'+str(len(lis))+'.img'