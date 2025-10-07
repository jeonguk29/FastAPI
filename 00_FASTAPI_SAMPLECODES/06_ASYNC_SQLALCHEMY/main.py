from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from typing import Optional


## 1. DB 접속
# 비동기 데이터베이스 설정을 위한 문자열을 정의합니다. 이 문자열에는 사용자 이름, 비밀번호, 서버 주소, 데이터베이스 이름이 포함되어 있습니다.
DATABASE_URL = ""  # 사용자의 데이터베이스 정보로 변경해야 합니다.

# SQLAlchemy의 비동기 엔진을 생성합니다. 
engine = create_async_engine(DATABASE_URL, echo=True)

## 2. 세션 정의
# 비동기 세션 생성을 위한 세션메이커를 정의합니다.
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

## 3. 세션 생성
# 비동기 데이터베이스 세션을 생성하고 관리하는 의존성 함수를 정의합니다.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()


## 4. 초기 테이블 생성
# SQLAlchemy의 모델 기본 클래스를 선언합니다. 이 클래스를 상속받아 데이터베이스 테이블을 정의할 수 있습니다.
Base = declarative_base()

class User(Base):
    # 'users' 테이블을 정의합니다.
    __tablename__ = 'users'
    # 각 열(column)을 정의합니다. id는 기본 키(primary key)로 설정됩니다.
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 사용자 이름, 중복 불가능하고 인덱싱합니다.
    email = Column(String(120))  # 이메일 주소, 길이는 120자로 제한합니다.
    

# Pydantic 모델을 정의합니다. 이 모델은 클라이언트로부터 받은 데이터의 유효성을 검사하는 데 사용됩니다.
class UserCreate(BaseModel):
    username: str
    email: str

# 자동으로 리소스 관리 해주는 컨텍스트 메니저 생성 (테이블 생성시 DB 접속 끝나면 DB 접속 해제 같은 걸 명시적 처리를 안하게 해줌)
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 로직
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 로직 (필요한 경우)
    
# FastAPI 애플리케이션을 초기화합니다.
app = FastAPI(lifespan=app_lifespan)

