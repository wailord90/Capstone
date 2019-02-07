from flask_bootstrap import Bootstrap
from models import *
# from pipenv.vendor.dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect
import os
import json
import pprint
import pusher 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# load_dotenv('.myenv')
# pprint.pprint(dict(os.environ))





app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_server_db'
Bootstrap(app)
print db

@app.route('/')
def index():
  return render_template('index.html')

class Example(db.Model):
	__tablename__ = 'example'
	id = db.Column('id', db.Integer, primary_key=True)
	data = db.Column('data', db.Unicode)

if __name__ == '__main__':
    app.run(debug=True)