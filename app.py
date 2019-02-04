from flask_bootstrap import Bootstrap
from models import *
# from pipenv.vendor.dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect
import os
import json
import pprint
import pusher 
from datetime import datetime

# load_dotenv('.myenv')
# pprint.pprint(dict(os.environ))

app = Flask(__name__)
Bootstrap(app)
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)