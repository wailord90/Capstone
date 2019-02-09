from flask_bootstrap import Bootstrap
from models import *
# from pipenv.vendor.dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect
import os
import json
import pprint
import pusher 
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table


engine = create_engine('mysql://BH6:password1@localhost/secure_sever_db', convert_unicode=True)
metadata = MetaData(bind=engine)
table = Table('table_name', metadata, autoload=True)
data = engine.execute('select * from table_name').first()

app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_sever_db'
Bootstrap(app)

@app.route('/archives')
def archive():
  return render_template('archive.html')
@app.route('/')
def index():
  return render_template('index.html',items=data)
@app.route('/logs')
def logs():
  return render_template('logs.html')
@app.route('/cameras')
def cameras():
  return render_template('cameras.html')


#class Example(db.Model):
#	__tablename__ = 'table_name'
#	data = db.Column('data', db.Unicode)

if __name__ == '__main__':
    app.run(debug=True)
