from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional


# 1. 데이터 베이스 연결
# mysql+pymysql://<username>:<password>@<host>:<port>/<dbname>
DATABASE_URL = "" #사용자의 데이터베이스 정보로 변경해야 합니다.
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
    username = Column(String(50), index=True)  # 사용자 이름, 중복 불가능하고 인덱싱합니다.
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

# 데이터 읽기
from sqlalchemy import func, desc

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 쿼리 실행
    db_users_count = db.query(User.username, func.count(User.id)).group_by(User.username).all()
    db_users_sum = db.query(User.username, func.sum(User.id)).group_by(User.username).all()
    db_users_max = db.query(User.username, func.max(User.id)).group_by(User.username).all()
    db_users_min = db.query(User.username, func.min(User.id)).group_by(User.username).all()

    # 결과를 딕셔너리 리스트로 변환
    print(db_users_count)
    for user_count in db_users_count:
        print(user_count)
    '''
    ('유지선', 3)
    ('정정욱', 3)
    튜플 형태임 보낼때 직렬화 클라에서 역직렬화 할때 튜플형태 정상적으로 동작하지 않아서
    아래 처럼 리스트안에 Json 형태로 만들어서 전달 해줌
    '''
    users_count = [{"username": username, "count": count} for username, count in db_users_count]
    users_sum = [{"username": username, "sum": sum} for username, sum in db_users_sum]
    users_max = [{"username": username, "max": max} for username, max in db_users_max]
    users_min = [{"username": username, "min": min} for username, min in db_users_min]

    # 결과 반환
    return {
        "users_count": users_count, 
        "users_sum": users_sum,
        "users_max": users_max,
        "users_min": users_min
    }

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

# Update 부분
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return {"error": "User not found"}
    
    if user.username is not None: # 클라가 넘겨준 값이 있다면
        db_user.username = user.username
    if user.email is not None:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user) #디비 반영 값을 해당 변수에 최신화
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}


# Delete 부분
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return {"error": "사용자를 찾을 수 없습니다"}
    db.delete(db_user)
    db.commit()
    return {"message": "사용자가 성공적으로 삭제되었습니다"}
