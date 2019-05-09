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
from db_orch import query_sessions, query_users, query_footage, import_archive


# engine = create_engine('mysql://BH6:password1@localhost/secure_sever_db', convert_unicode=True)
# metadata = MetaData(bind=engine)
# table = Table('table_name', metadata, autoload=True)
# data = engine.execute('select * from table_name').first()

app = Flask(__name__, static_url_path='/static')

Bootstrap(app)


@app.route('/SecureServerRoom.com/archives')
def archive():
    footage = query_footage()
    json_footage = [d.__dict__ for d in footage]
    if request.method == "POST":
        video = request.form['submit_button']
        return render_template('footage.html', video=str(video+".mp4"))
    return render_template('archive.html',footage= json_footage)


@app.route('/SecureServerRoom.com/')
def index():
    sessions = query_sessions()
    json_sessions = [d.__dict__ for d in sessions]
    users = query_users()
    json_users = [d.__dict__ for d in users]
    session_length = len(json_sessions)-1
    time2 = pretty_date(sessions[session_length-1].time)
    time1 = pretty_date(sessions[session_length].time)
    time3 = pretty_date(sessions[session_length-2].time)
    time4 = pretty_date(sessions[session_length-3].time)
    return render_template('index.html', users=json_users, session_length=session_length, sessions=json_sessions, time1=time1, time2=time2, time3=time3, time4=time4)


@app.route('/SecureServerRoom.com/logs', methods=["GET", "POST"])
def logs():

    if request.method == "POST":
        filterhost = ""

        if request.form['submit_button'] == 'jeremycamera-VirtualBox':
            filterhost = 'jeremycamera-VirtualBox'
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
        return render_template("logs.html", sessions=tmp, host=filterhost)

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
        # init camera
    camera = cv2.VideoCapture(0)
    # camera.set(3, 320)   uncommenting these causes an error
    # camera.set(4, 240)   making the video created unusable
    time.sleep(0.5)  # gives camera time to initialize (jeremy)

    # master frame
    master = None
    didmove = False

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('videos/output.mp4', fourcc, 10.0, (640, 480))
    while (True):
        ret, preFrame = camera.read()
        while(1):
            grabbed, frame0 = camera.read()

            if not grabbed:  # error handle (jeremy)
                break

            # gray frame
            frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

            # blur frame
            frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

            # initialize master
            if master is None:
                master = frame2
                continue

            # delta frame
            frame3 = cv2.absdiff(master, frame2)

            # threshold frame
            frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes
            kernel = numpy.ones((5, 5), numpy.uint8)
            frame5 = cv2.dilate(frame4, kernel, iterations=4)

            # find contours on thresholded image
            contours, nada = cv2.findContours(
                frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # make coutour frame
            frame6 = frame0.copy()

            # target contours
            targets = []

            # loop over the contours
            for c in contours:

                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 500:
                    continue

                x, y, w, h = cv2.boundingRect(c)
                rx = x + int(w / 2)
                ry = y + int(h / 2)
                ca = cv2.contourArea(c)

                # save target contours
                targets.append((rx, ry, ca))

            if targets:
                out.write(frame0)
                if not didmove:
                    didmove = True
            imgencode = cv2.imencode('.jpg', frame0)[1]
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
            # update master
            master = frame2

    # release video and camera
    camera.release()
    out.release()
    cv2.destroyAllWindows()
    if didmove:
        date = datetime.datetime.now()
        add_footage(date, 'none')
        os.system("ffmpeg -i ./videos/output.mp4 -vcodec libx264 -acodec aac " +
                  date.strftime("%m_%d_%Y_%H_%M_%S")+".mp4")


@app.route('/SecureServerRoom.com/changed')
def calc():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
