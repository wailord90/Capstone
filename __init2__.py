from flask_bootstrap import Bootstrap
from models import *
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


# engine = create_engine('mysql://BH6:password1@localhost/secure_sever_db', convert_unicode=True)
# metadata = MetaData(bind=engine)
# table = Table('table_name', metadata, autoload=True)
# data = engine.execute('select * from table_name').first()

app = Flask(__name__,static_url_path='/static')
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@localhost/secure_sever_db'
Bootstrap(app)

#camera2=cv2.VideoCapture(0) #this makes a web cam object

@app.route('/archives')
def archive():
  return render_template('archive.html')
@app.route('/')
def index():
  return render_template('index.html',items="data")
@app.route('/logs')
def logs():
  return render_template('logs.html')
@app.route('/SecureServerRoom.com/cameras')
def cameras():
  return render_template('cameras.html')

def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1

def get_frame():
	# init camera
	camera = cv2.VideoCapture(0)
	#camera.set(3, 320)   uncommenting these causes an error
	#camera.set(4, 240)   making the video created unusable
	time.sleep(0.5) #gives camera time to initialize (jeremy)

	# master frame
	master = None

	# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi',fourcc, 10.0, (640,480))
	f= open("aaaa.txt","w+")
	a=datetime.now()
  	f.write("%s\r\n" % a)
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
			contours, nada = cv2.findContours(frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			# make coutour frame
			frame6 = frame0.copy()

			# target contours
			targets = []

			# loop over the contours
			for c in contours:

			    # if the contour is too small, ignore it
			    if cv2.contourArea(c) < 500:
				continue

			    # contour data
			    M = cv2.moments(c)  # ;print( M )
			    cx = int(M['m10'] / M['m00'])
			    cy = int(M['m01'] / M['m00'])
			    x, y, w, h = cv2.boundingRect(c)
			    rx = x + int(w / 2)
			    ry = y + int(h / 2)
			    ca = cv2.contourArea(c)

			    # plot contours
			    cv2.drawContours(frame6, [c], 0, (0, 0, 255), 2)
			    cv2.rectangle(frame6, (x, y), (x + w, y + h), (0, 255, 0), 2)
			    cv2.circle(frame6, (cx, cy), 2, (0, 0, 255), 2)
			    cv2.circle(frame6, (rx, ry), 2, (0, 255, 0), 2)

			    # save target contours
			    targets.append((rx, ry, ca))

			# make target
			area = sum([x[2] for x in targets])
			mx = 0
			my = 0
			if targets:
			    for x, y, a in targets:
				mx += x
				my += y
			    mx = int(round(mx / len(targets), 0))
			    my = int(round(my / len(targets), 0))

			# plot target
			tr = 50
			frame7 = frame0.copy()
			if targets:
			    out.write(frame0)
			    cv2.circle(frame7, (mx, my), tr, (0, 0, 255, 0), 2)
			    cv2.line(frame7, (mx - tr, my), (mx + tr, my), (0, 0, 255, 0), 2)
			    cv2.line(frame7, (mx, my - tr), (mx, my + tr), (0, 0, 255, 0), 2)
			imgencode=cv2.imencode('.jpg',frame0)[1]
			stringData=imgencode.tostring()
			yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
			# update master
			master = frame2

        #release video and camera
    	camera.release()
    	out.release()
    	cv2.destroyAllWindows()



@app.route('/changed')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

#class Example(db.Model):
#	__tablename__ = 'table_name'
#	data = db.Column('data', db.Unicode)

if __name__ == '__main__':
    app.run(debug=True)
    
