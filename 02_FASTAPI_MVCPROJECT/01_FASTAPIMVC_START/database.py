from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:ju12291229%40%40@localhost:3306/my_memo_app"

engine = create_engine(DATABASE_URL)

# 세션 메이커를 사용하여 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()