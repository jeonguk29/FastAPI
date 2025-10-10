from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})
# Jinja2Template 사용시 TemplateResponse는 request객체가 필요하다고 했음
# 이는 내부적으로 사용자의 요청과 관련된 데이터를 템플릿에 전달하기 위함임

@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}