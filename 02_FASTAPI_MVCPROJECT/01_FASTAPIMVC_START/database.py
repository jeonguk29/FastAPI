from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
DB 접속, 세션 정리 비동기 변환
'''
DATABASE_URL = "mysql+aiomysql://root:ju12291229%40%40@localhost:3306/my_memo_app"

engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 메이커를 사용하여 세션 생성
AsyncSessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine,
                            class_= AsyncSession
                            ) # 비동기 세션 설정

Base = declarative_base()