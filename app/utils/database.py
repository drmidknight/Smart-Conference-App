from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from .config import settings
from typing import Any

#POSTGRESSQL_URL = "postgresql+psycopg2://username:password@localhost/database_name"@
#MYSQL_URL = "mysql+pymysql://root:@localhost:3307/smart_conference_app?charset=utf8"
#MYSQL_URL = "mysql+pymysql://root:Openforme@localhost:3307/fastapi_student_results?charset=utf8"


metadata_obj = MetaData()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, 
                       pool_size=settings.POOL_SIZE, 
                       pool_recycle=settings.POOL_RECYCLE,
                       pool_timeout=settings.POOL_TIMEOUT, 
                       max_overflow=settings.MAX_OVERFLOW, 
                       connect_args=settings.connect_args)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)


@as_declarative()
class Base:
    id: Any



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





class Database():
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None

    def get_db_connection(self):
        if self.connection_is_active == False:

            try:
                self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_size=settings.POOL_SIZE, pool_recycle=settings.POOL_RECYCLE,
                        pool_timeout=settings.POOL_TIMEOUT, max_overflow=settings.MAX_OVERFLOW, connect_args=settings.connect_args)
                return self.engine
            except Exception as ex:
                print("Error connecting to DB : ", ex)
        return self.engine

    def get_db_session(self,engine):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as ex:
            print("Error getting DB session : ", ex)
            return None