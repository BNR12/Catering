"""

Brittany Regrut
BNR12
CS1520
HW 2

"""

import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import db, User, Event


#create application
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='owner',
	PASSWORD='pass',

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
))

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	print('Initialized the database.')

#main url
#clear session and redirect to login
@app.route('/')
def main_page():
	if "username" in session:
		session.clear()
	return redirect(url_for('login'))

#login
#on POST, if owner is logging in, redirect to owner page
#else, test against database to find if user exists
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == app.config['USERNAME']:
			if request.form['password'] == app.config['PASSWORD']:
				session['username'] = app.config['USERNAME']
				return redirect(url_for("owner"))
		else:
			error='invalid login'
	return render_template('login.html', error=error)

#logout
@app.route('/logout')
def logout():
	session.clear()
	flash('You were logged out')
	return redirect(url_for('login'))

#route for owner page
#can only be accessed if the owner is logged in, otherwise redirects to login
@app.route('/owner')
def owner():
	if 'username' in session:
		if session['username']==app.config['USERNAME']:
			events = Event.query.all()
			return render_template('owner.html', events=events)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

#route for creating accounts
@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		#get form input and create a new account
		#if owner is logged in, will be creating staff accounts
		if 'username' in session:
			if session['username']==app.config['USERNAME']:
				user = 1
		else:
			#otherwise will be creating a customer account
			user = 2
		new = User(user, request.form['username'], request.form['password'])
		db.session.add(new)
		db.session.commit()
		flash('User created')
		#return to owner page or login
		if user == 1:
			return redirect(url_for('create'))
		else:
			return redirect(url_for('login'))
	else:
		return render_template('create.html', error='none')

#route for requesting an event
#need to add check to verify this is a customer requesting an event and not a staff/owner account
@app.route('/requeste', methods=['GET', 'POST'])
def requeste():
	if 'username' in session:
		if request.method == 'GET':
			return render_template('request.html')
		else:
			#currently does not handle duplicate date request
			new = Event(request.form['date'], session['username'])
			db.session.add(new)
			db.session.commit()
			flash('Event Created')
			return render_template('request.html')
	else:
		return redirect(url_for('login'))

