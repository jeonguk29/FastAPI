from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional


# 1. 데이터 베이스 연결
# mysql+pymysql://<username>:<password>@<host>:<port>/<dbname>
DATABASE_URL =  # 사용자의 데이터베이스 정보로 변경해야 합니다.
engine = create_engine(DATABASE_URL) 


'''
SQL
- 스키마 생성
- 테이블에 데이터를 넣고 빼는
- ID/ 권한

sqlalchemy를 사용하면 위 기능을 파이썬에서 사용 할 수 있음
sqlalchemy는 테이블 까지도 모두 객체로 관리함 즉 데이터베이스에 CRUD를 하려면 테이블 객체를 먼저 만들어서 가지고 있어야함
'''
# 2. sqlalchemy의 모델 기본 클래스를 선언, 이 클래스를 상속받아 DB 테이블을 정의할 수 있음
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 사용자 이름, 중복 불가능하고 인덱싱합니다.
    email = Column(String(120))  # 이메일 주소, 길이는 120자로 제한합니다.

class UserCreate(BaseModel):
    username: str
    email: str

# 데이터베이스 세션을 생성하고 관리하는 의존성 함수를 정의함
def get_db():
    db = Session(bind=engine) #engine이 mysql 접속하는 객체 
    try:
        yield db
    finally:
        db.close()

# DB엔젠을 사용하여 모델을 기반으로 테이블을 생성합니다. (테이블이 없다면 생성함)
Base.metadata.create_all(bind=engine)

# 3. FastAPI 애플리케이션을 초기화
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# 사용자를 생성하는 POST API 엔드포인트를 추가
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #DB를 쓰는 API라면  db: Session = Depends(get_db) 이부분을 써주면 된다.
    new_user = User(username=user.username, email=user.email)
    db.add(new_user) # 생성된 User 인스턴스를 데이터베이스 세션에 추가합니다.
    db.commit() # 데이터베이스에 대한 변경사항을 커밋합니다.
    db.refresh(new_user) # 데이터베이스로 부터 새 User 인스턴스의 최신 정보를 가져옵니다. (실제 DB 레코드 값으로 Update)

    # 새로 생성된 사용자 정보를 반환합니다.
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
