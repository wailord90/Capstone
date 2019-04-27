from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'app2.db'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////etc/secureserver.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    username = db.Column(db.String)
    phonenumber = db.Column(db.String)

    def __repr__(self):
        return '|%r|%r|%r|%r|%r|' % (self.email, self.password, self.authenticated, self.username, self.phonenumber)


class Archived(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '|%r|%r|%r|%r|%r|%r|%r|%r|' % (self.path, self.date, self.flag)


class Archived_User_Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), nullable=False)
    auid = db.Column(db.String(80), nullable=False)
    cwd = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    pid = db.Column(db.String(80), nullable=False)
    a2 = db.Column(db.String(80), nullable=False)
    cmd = db.Column(db.String(80), nullable=False)
    host = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '|%r|%r|%r|%r|%r|%r|%r|%r|' % (self.time, self.uid, self.auid, self.cwd, self.pid, self.a2, self.cmd, self.host)


class User_Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), nullable=False)
    auid = db.Column(db.String(80), nullable=False)
    cwd = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    pid = db.Column(db.String(80), nullable=False)
    a2 = db.Column(db.String(80), nullable=False)
    cmd = db.Column(db.String(80), nullable=False)
    host = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '|%r|%r|%r|%r|%r|%r|%r|%r|%r|' % (self.time, self.uid, self.auid, self.cwd, self.pid, self.a2, self.cmd, self.host, self.flag)


class footage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '|%r|%r|' % (self.date, self.usr)
