from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = None
Session = None


def init_db(config):
    global engine, Session
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'],
                           pool_timeout=config['SQLALCHEMY_POOL_TIMEOUT'],
                           pool_size=config['SQLALCHEMY_POOL_SIZE'],
                           pool_recycle=config['SQLALCHEMY_POOL_RECYCLE'])
    engine.execute("SET NAMES utf8mb4;")
    Session = sessionmaker(engine)
