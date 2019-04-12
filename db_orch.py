from sql_connection import User_Sessions,db
from datetime import datetime


def add_session(time,username):
    datetime_object = datetime.strptime(time, '%b %d %Y %I:%M%p')
    user_sess = User_Sessions(date=datetime_object,user=username)
    db.session.add(user_sess)
    db.session.commit()

def query_sessions():
    return User_Sessions.query.all()

def query_filtered_sessions(fil):
    return User_Sessions.query.filter_by(username=fil).first()


