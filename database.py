from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, scoped_session

user_name = "root"
user_pwd = "1234"
db_host = "127.0.0.1"
db_name = "dydgh"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_pwd,
    db_host,
    db_name,
)

engine  =create_engine(   #접속?
    DATABASE,
    encoding ="utf-8",
    echo =True
)
# engine = create_engine(
#     DATABASE, connect_args={"check_same_thread": False}
# )


session = scoped_session(
    sessionmaker(
        autocommit =False,
        autoflush=False,
        bind= engine 
    )

)
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()  ##인스턴트생성
# Base.query = session.query_property() 
