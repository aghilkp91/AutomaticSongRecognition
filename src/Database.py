from sqlalchemy import Column, String, Integer, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .Config import ASRConfig
from sqlalchemy.exc import ProgrammingError, DatabaseError, SQLAlchemyError

# # 创建对象的基类:
Base = declarative_base()


def checkDatabase(conn=ASRConfig.sqldb_url):
    try:
        engine = create_engine(conn)
        DBSession = sessionmaker(bind=engine)
        dbs = DBSession()
        dbs.query(Songs).first()
        dbs.query(Fingerprints).first()
        return (True,0,"")
    except ProgrammingError as err:
        return (False,err.code,err.orig)
    except DatabaseError as err:
        return (False, err.code, err.orig)

def initSession(conn=ASRConfig.sqldb_url):
    # init connection
    engine = create_engine(conn, pool_size=ASRConfig.mysql_max_connection)
    # create sessionmaker:
    #DBSession = sessionmaker(bind=engine)
    DBSession = sessionmaker(bind=engine,autoflush=False, expire_on_commit=False)

    return DBSession, engine


def createTables(conn=ASRConfig.sqldb_url):
    try:
        engine = create_engine(conn)
        Base.metadata.create_all(engine)
        return True
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error

class Songs(Base):
    # Table name:
    __tablename__ = 'Songs'

    # Table structure:
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(64))
    # moviename = Column(String(64))
    filehash = Column(String(512), index=True)
    fingerprinted = Column(Boolean, default=False)


class Fingerprints(Base):
    # Table name:
    __tablename__ = 'Fingerprints'

    # Table structure:
    id = Column(Integer, autoincrement=True, primary_key=True)
    song_id = Column(Integer,index=False)
    # length of string depend ono how long your fingerprint is.
    fingerprint = Column(String(64), index=True)
    offset = Column(Integer)
