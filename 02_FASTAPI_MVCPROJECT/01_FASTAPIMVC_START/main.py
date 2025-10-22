from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from database import Base, engine # 동일 폴더에 있는 파이썬 코드는 해당 파일명만 넣으면 클래스나 객체 임포트 가능
from controllers import router
from contextlib import asynccontextmanager
 

# 자동으로 리소스 관리 해주는 컨텍스트 메니저 생성 (테이블 생성시 DB 접속 끝나면 DB 접속 해제 같은 걸 명시적 처리를 안하게 해줌)
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 로직
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 로직 (필요한 경우)

# Fast API 애플리케이션 초기화
# Swagger UI와 Redoc 또한 비활성화=
app = FastAPI(lifespan=app_lifespan, docs_url=None, redoc_url=None)
# 세션을 위한 middleware 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
# 프론트 부분을 제어하기 위한 Jinja2Templates 코드 추가
templates = Jinja2Templates(directory="templates")
# API 관련 라우터 등록
app.include_router(router)

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

    