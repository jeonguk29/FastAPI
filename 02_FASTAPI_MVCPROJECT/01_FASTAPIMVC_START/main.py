from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from database import Base, engine # 동일 폴더에 있는 파이썬 코드는 해당 파일명만 넣으면 클래스나 객체 임포트 가능

app = FastAPI()

# 세션을 위한 middleware 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
# 데이터 베이스에 테이블이 없다면 자동 생성을 위한 코드 추가
Base.metadata.create_all(bind=engine)
# 프론트 부분을 제어하기 위한 Jinja2Templates 코드 추가
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

    