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
import pymysql
import re
# load_dotenv('.myenv')
# pprint.pprint(dict(os.environ))





app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_sever_db'
Bootstrap(app)

def news():
    host='localhost'
    user = 'root'
    password = 'password'
    db = 'secure_sever_db'

    try:
        con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
     except Exception as e:
        sys.exit('error',e)

     cur = con.cursor()
     cur.execute("SELECT * FROM dataset")
     data = cur.fetchall()
    return data
    #  for row in data:
    #      video = row[0]
    #      logs = row[1]
    #      print('===============================================')
    #      print('Video', video)
    #      print('Logs :', logs)
    #      print('===============================================')

@app.route('/archives')
def archive():
  return render_template('archive.html')
@app.route('/')
def index():
  data = news()
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