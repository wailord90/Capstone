from sql_connection import User_Sessions, db
from datetime import datetime


def create_db():
    db.create_all()


def add_session(time, uid, auid, cwd, pid, a2):
    datetime_object = datetime.strptime(time, '%m/%d/%Y %H:%M:%S.%f')
    user_sess = User_Sessions(time=datetime_object,
                              uid=username, auid=auid, cwd=cwd, pid=pid, a2=a2)
    db.session.add(user_sess)
    db.session.commit()


def query_sessions():
    return User_Sessions.query.all()


def query_filtered_sessions(fil):
    return User_Sessions.query.filter_by(username=fil).first()
