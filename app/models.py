from sqlalchemy import Column, DateTime, Integer, String, BigInteger, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
from datetime import datetime
import sqlalchemy.exc as exc
import config

logger = logging.getLogger('manager.models')
Base = declarative_base()
DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
Session_ = None


class VideoXng(Base):
    __tablename__ = 'video_xng'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    album_id = Column(BigInteger, unique=True)
    title = Column(String(600))
    producer = Column(String(50))
    url = Column(String(500))
    v_url = Column(String(500))
    hurl = Column(String(500))
    views = Column(Integer)
    cover_watermark = Column(String(500))
    total = Column(Integer)
    comment_count = Column(Integer)
    du = Column(Integer)
    create_time = Column(DateTime, default=datetime.now())


def make_db():
    global Session_
    try:
        engine = create_engine(DATABASE_URI)
        DB = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        Session_ = DB()
    except Exception as e:
        logger.error(e, exc_info=True)


def DBSession(temp, video_type):
    session = Session_

    video = VideoXng()
    video.album_id = temp['album_id']
    video.title = temp['title']
    video.producer = temp['user']['nick']
    video.url = temp['url']
    video.v_url = temp['v_url']
    video.hurl = temp['user']['hurl']
    video.views = temp['views']
    video.cover_watermark = temp['cover_watermark']
    video.total = temp['favor']['total']
    video.comment_count = temp['comment_count']
    video.du = temp['du']
    video.type = video_type
    try:
        session.add(video)
        session.commit()
    except exc.IntegrityError as e:
        logger.error('video exist already')
        session.rollback()
    except Exception as e:
        logger.exception(e)
        session.rollback()
    session.close()


if __name__ == '__main__':
    import json
    make_db()
    with open('temp.json', 'r') as f:
        temp = json.load(f)
    DBSession(temp, 0)