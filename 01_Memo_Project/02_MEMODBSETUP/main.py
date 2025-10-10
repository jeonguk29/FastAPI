from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATABASE_URL = "mysql+pymysql://root:ju12291229%40%40@localhost:3306/my_memo_app"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 데이터 베이스 테이블 생성
class Memo(Base):
    __tablename__ = 'memo'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))

# 클라측 요청 객체 정의    
class MemoCreate(BaseModel):
    title: str
    content: str
    
class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 자동으로 DB 사용 끝나면 세션 끊어주기
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# 테이블 없으면 생성        
Base.metadata.create_all(bind=engine)
    
# 메모 생성
@app.post("/memos/")
async def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    new_memo = Memo(title=memo.title, content=memo.content)
    db.add(new_memo) #레코드 추가
    db.commit()
    db.refresh(new_memo)
    return ({"id": new_memo.id, "title": new_memo.title, "content": new_memo.content})

# 메모 조회
@app.get("/memos/")
async def list_memos(db: Session = Depends(get_db)):
    memos = db.query(Memo).all()
    return [{"id": memo.id, "title": memo.title, "content": memo.content} for memo in memos]
    # 반환 리스트 컴프리핸션으로 전체 레코드 반환
    
# 메모 수정
@app.put("/memos/{memo_id}")
async def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if db_memo is None:
        return ({"error": "Memo not found"})

    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content
        
    db.commit()
    db.refresh(db_memo)
    return ({"id": db_memo.id, "title": db_memo.title, "content": db_memo.content})

# 메모 삭제
@app.delete("/memos/{memo_id}")
async def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if db_memo is None:
        return ({"error": "Memo not found"})
        
    db.delete(db_memo)
    db.commit()
    return ({"message": "Memo deleted"})


# 기존 라우트
@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}