from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from typing import Optional


# 1. 데이터 베이스 연결
# mysql+pymysql://<username>:<password>@<host>:<port>/<dbname>
DATABASE_URL =  # 사용자의 데이터베이스 정보로 변경해야 합니다.
engine = create_engine(DATABASE_URL) 


# FastAPI 애플리케이션 인스턴스를 생성하여 앱을 초기화합니다.
app = FastAPI()

# SessionLocal 인스턴스를 생성하기 위한 factory를 정의합니다.
# autocommit과 autoflush를 False로 설정하여, 
# 데이터베이스 세션 관리를 더욱 세밀하게 제어할 수 있습니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 Base 클래스를 상속받아 모델의 기본 클래스를 생성합니다.
Base = declarative_base()

# User 모델을 정의합니다. 이 클래스는 데이터베이스의 'users' 테이블에 매핑됩니다.
class User(Base):
    __tablename__ = 'users'  # 데이터베이스의 테이블 이름을 지정합니다.
    id = Column(Integer, primary_key=True, index=True)  # 사용자의 ID로, 기본 키로 설정됩니다.
    username = Column(String(50), unique=True, index=True)  # 사용자명은 최대 50자로, 고유해야 합니다.
    email = Column(String(120))  # 사용자의 이메일 주소로, 최대 120자까지 허용됩니다.

# Pydantic 모델을 정의합니다. 이 모델은 클라이언트로부터 받은 데이터의 유효성을 검사하는 데 사용됩니다.
class UserCreate(BaseModel):
    username: str
    email: str
    
# SQLAlchemy를 사용하여 데이터베이스에 테이블을 생성합니다. 
# 만약 테이블이 이미 존재한다면, 아무런 작업도 수행하지 않습니다.
Base.metadata.create_all(bind=engine)

# '/users/' 경로에 POST 요청을 받는 엔드포인트를 생성합니다.
# 이 함수는 새로운 사용자를 생성하고 데이터베이스에 저장하는 역할을 합니다.
@app.post("/users/")
def create_user(user: UserCreate):
    # SessionLocal()을 호출하여 데이터베이스 세션을 생성합니다.
    db = SessionLocal()
    # User 인스턴스를 생성하고 초기화합니다.
    db_user = User(username=user.username, email=user.email)
    # 세션에 User 인스턴스를 추가합니다.
    db.add(db_user)
    # 변경 사항을 데이터베이스에 커밋합니다.
    db.commit()
    # 커밋된 User 인스턴스의 최신 정보를 데이터베이스로부터 불러옵니다.
    db.refresh(db_user)
    # 데이터베이스 작업이 끝났으므로 세션을 닫습니다. 
    # Depends 방식 같은 경우는 DB 세션을 생성하고 관리하는 의존성 함수를 정의 했어서 자동으로 끊어줬음
    db.close()
    # 생성된 사용자의 정보를 JSON 형식으로 반환합니다.
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}