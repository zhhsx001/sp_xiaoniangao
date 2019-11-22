from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()
metadata = Base.metadata


class VideoXng(Base):
    __tablename__ = 'video_xng'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    album_id = Column(Integer, unique=True)
    title = Column(String(600))
    producer = Column(String(50))
    url = Column(String(500))
    v_url = Column(String(500))
    hurl = Column(String(500))
    views = Column(Integer)
    cover_watermark = Column(String(5))
    total = Column(Integer)
    comment_count = Column(Integer)
    du = Column(Integer)
    create_time = Column(DateTime, default=datetime.datetime.now())