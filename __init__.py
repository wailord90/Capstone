from flask_bootstrap import Bootstrap
# from pipenv.vendor.dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, Response
import os
import json
import pprint
import pusher
import cv2
import sys
import numpy
import time
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table
from db_orch import query_sessions


# engine = create_engine('mysql://BH6:password1@localhost/secure_sever_db', convert_unicode=True)
# metadata = MetaData(bind=engine)
# table = Table('table_name', metadata, autoload=True)
# data = engine.execute('select * from table_name').first()

app = Flask(__name__, static_url_path='/static')
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_sever_db'
Bootstrap(app)

# camera2=cv2.VideoCapture(0) #this makes a web cam object


@app.route('/archives')
def archive():
    return render_template('archive.html')


@app.route('/')
def index():
    return render_template('index.html', items="data")


@app.route('/logs')
def logs():
    sessions = query_sessions()
    json_sessions = [d.__dict__ for d in sessions]
    return render_template('logs.html', sessions=json_sessions)


@app.route('/SecureServerRoom.com/cameras')
def cameras():
    return render_template('cameras.html')


def gen():
    i = 1
    while i < 10:
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i += 1


def get_frame():
    #global camera2
    # del(camera2)
    camera = cv2.VideoCapture(0)  # this makes a web cam object
    #global camera
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 8.0, (640, 480))
    #cap = cv2.VideoCapture(0)

    while(True):

        ret, frame2 = camera.read()  # frame 2 is current frame

        if ret == True:  # if camera is working
            out.write(frame2)  # write the current frame to the video file
            imgencode = cv2.imencode('.jpg', frame2)[1]
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    # release video and camera
    out.release()
    camera.release()


@app.route('/changed')
def calc():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
# class Example(db.Model):
#	__tablename__ = 'table_name'
#	data = db.Column('data', db.Unicode)


if __name__ == '__main__':
    app.run(debug=True)
