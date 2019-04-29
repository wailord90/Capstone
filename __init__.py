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
from time_convert import pretty_date
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
    sessions = query_sessions()
    json_sessions = [d.__dict__ for d in sessions]
    session_length = len(json_sessions)-1
    time2 = pretty_date(sessions[session_length-1].time)
    time1 = pretty_date(sessions[session_length].time)
    time3 = pretty_date(sessions[session_length-2].time)
    time4 = pretty_date(sessions[session_length-3].time)
    return render_template('index.html', session_length=session_length, sessions=json_sessions, time1=time1, time2=time2, time3=time3, time4=time4)


@app.route('/logs', methods=["GET", "POST"])
def logs():

    if request.method == "POST":
        filterhost = ""

        if request.form['submit_button'] == 'capstone_1':
            filterhost = 'capstone_1'
            pass  # do something
        elif request.form['submit_button'] == 'capstone_2':
            filterhost = 'capstone_2'
            pass  # do something else
        elif request.form['submit_button'] == 'capstone_3':
            filterhost = 'capstone_3'
            pass  # do something else
        sessions = query_sessions()
        json_sessions = [d.__dict__ for d in sessions]
        tmp = []
        for x in json_sessions:
            print x['host']
            if str(x['host']).strip() == filterhost:
                tmp.append(x)
        return render_template("logs.html", sessions=tmp)

    return render_template('hosts.html')


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
