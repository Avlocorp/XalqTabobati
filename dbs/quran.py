from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os


SQLALCHEMY_DATABASE_URL = os.environ.get('MYSQL_DSN')
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/quran_micraservice"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class suraName(Base):
    __tablename__ = 'quran_suras'

    id = Column(Integer, primary_key=True, index=True)
    sura_name = Column(String)

class quranText(Base):
    __tablename__ = 'quran_ayas'

    id = Column(Integer, primary_key=True, index=True)
    sura = Column(Integer)
    aya = Column(Integer)
    text = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
