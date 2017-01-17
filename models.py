from flask_sqlalchemy import SQLAlchemy

# note this should only be created once per project
# to define models in multiple files, put this in one file, and import db into each model, as we import it in catering.py
db = SQLAlchemy()

class User(db.Model):
	type = db.Column(db.Integer, nullable=False)
	username = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(20), nullable=False)

	def __init__(self, type, username, password):
		self.type = type
		self.username = username
		self.password = password

	def __repr__(self):
		return '<Username {}>'.format(self.username)

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date, nullable=False)
	#requested by (username)
	by = db.Column(db.String(20), nullable=False)
	#number of staff scheduled
	num = db.Column(db.Integer, default=0)
	staff1 = db.Column(db.String(20), nullable=True, default=None)
	staff2 = db.Column(db.String(20), nullable=True, default=None)
	staff3 = db.Column(db.String(20), nullable=True, default=None)

	def __init__(self, date, by):
		self.date = date
		self.by = by


	def __repr__(self):
		return '<Event {} on {}. Staff working: {}>'.format(self.id, self.date, self.num)