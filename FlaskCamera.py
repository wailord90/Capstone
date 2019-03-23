#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import sys
import numpy


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cameras.html')

def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1

def get_frame():

    camera=cv2.VideoCapture(0) #this makes a web cam object
  

    while True:
        ret, frame = camera.read()
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
 

    del(camera)

@app.route('/changed')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
