from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates") #이걸 사실 안써도 됨 기본 문법으로 선언 되어 있음

@app.get("/")
def read_root(request: Request): #Request는 사용자가 요청할때 헤더부터 바디까지 가지고 있는 전체 데이터
    return templates.TemplateResponse("index.html", {"request": request, "username": "JeongUk"})