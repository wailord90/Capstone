from sql_connection import User_Sessions, db
from datetime import datetime


def create_db():
    db.create_all()

def add_session(time, uid, auid, cwd, pid, a2, cmd, hostname, flag):
    datetime_object = datetime.strptime(time, '%m/%d/%Y %H:%M:%S.%f')
    user_sess = User_Sessions(time=datetime_object,
                              uid=uid, auid=auid, cwd=cwd, pid=pid, a2=a2, cmd=cmd,hostname=hostname,flag=flag)
    db.session.add(user_sess)
    db.session.commit()


def query_sessions():
    return User_Sessions.query.all()

def delete_sessions():
  return User_Sessions.query().delete()

def query_filtered_sessions(fil):
    return User_Sessions.query.filter_by(uid=fil).first()
