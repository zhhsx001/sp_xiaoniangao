from sqlalchemy import Column, DateTime, Integer, String, BigInteger, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
from datetime import datetime
from mysql.connector.errors import IntegrityError

logging.basicConfig(filename='data/sp_xiaoniangao.log', level=logging.INFO)
Base = declarative_base()
DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/sp_xiaoniangao?charset=utf8mb4'
Session = None


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
    global Session
    try:
        engine = create_engine(DATABASE_URI)
        DB = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        Session = DB()
    except Exception as e:
        logging.error('sp_xiaoniangao/models class make_db: get database error----', e)


def DBSession(temp, video_type):
    session = Session

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
    except Exception as e:
        logging.error('sp_xiaoniangao/models class DBSession: session.add error----', e)
    try:
        session.commit()
    except IntegrityError as e:
        logging.error('video exist already')
    except Exception as e:
        logging.error('sp_xiaoniangao/models class DBSession: session.commit error----', e)
        session.rollback()
    session.close()