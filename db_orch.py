from sql_connection import User_Sessions, db, Archived, Users
from datetime import datetime
import os


def backup(date):
    os.system("sqlite3 secureserver.db ".dump 'user__sessions'" | grep '^INSERT' > user_logs"+date+".db")


def import_archive(date):
    os.system("tmp=$(user_logs"+date +
              ".sql);echo'${tmp//user__sessions/archived__user__sessions}' | sqlite3 secureserver.db")


def create_db():
    db.create_all()


def add_session(time, uid, auid, cwd, pid, a2, cmd, host, flag):
    datetime_object = datetime.strptime(time, '%m/%d/%Y %H:%M:%S.%f')
    user_sess = User_Sessions(time=datetime_object,
                              uid=uid, auid=auid, cwd=cwd, pid=pid, a2=a2, cmd=cmd, host=host, flag=flag)
    db.session.add(user_sess)
    db.session.commit()


def archive(activity, date, flag):
    now = datetime.datetime.today()
    archived = Archived(date=now, activity=activity, flag=flag)
    db.session.add(archived)
    db.session.commit()


def add_user(email, password, authenticated, username, phonenumber):
    now = datetime.datetime.today()
    user = Users(email=email, password=password, authenticated=authenticated,
                 username=username, phonenumber=phonenumber)
    db.session.add(user)
    db.session.commit()


def query_users():
    return Users.query().all()


def query_sessions():
    return User_Sessions.query.all()


def delete_sessions():
    return User_Sessions.query().delete()


def query_filtered_sessions(fil):
    return User_Sessions.query.filter_by(uid=fil).first()
