from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os
db_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'app2.db'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////etc/test.db'
db = SQLAlchemy(app)


class User_Sessions(db.Model):
        id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime,nullable=False)
	user = db.Column(db.String(80),nullable=False)
        def __repr__(self):
            return '|%r|%r|' % (self.date,self.user)

