from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

# class Archive(Base):
#   __tablename__ = 'archives'
#   id = Column(Integer, primary_key=True)
#   video = Column(String(120))
#   date = Column(DateTime, default=datetime.utcnow)
#   status = Column(String(120))

#   def __init__(self, video=None, date=None, status=None):
#     self.video = video
#     self.date = date
#     self.status = status

#   def __repr__(self):
#     return '<Archive %r>' % (self.video)