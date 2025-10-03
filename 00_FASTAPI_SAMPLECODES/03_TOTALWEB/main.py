from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()


"""
mount로 경로를 단축 시켜서 templates 폴더에서 /img만 사용하더라도 경로 연결 되게 설정
백엔드 개발을 웹사이트를 보여줄때 이런 이런 구조로 사용하면 편함
"""
app.mount("/img", StaticFiles(directory="static/img"), name="img")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})