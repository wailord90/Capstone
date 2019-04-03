from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_server:3333'
db = SQLAlchemy(app)
Example(db)


class Example(db.Model):
	__tablename__ = 'user_sessions'
	date = db.Column('date', db.Integer)
	user = db.Column('user', db.Unicode)
	console.log("here")